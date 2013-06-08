import glob2
from git import *
import requests
from whoosh.index import create_in
from whoosh.fields import Schema, ID, KEYWORD, TEXT
from whoosh.query import *
from settings import ON_DUTY
from urllib import quote

faq_schema = Schema(path=ID(unique=True, stored=True),
                    title=TEXT(stored=True), \
                    tags=KEYWORD(stored=True),
                    body=TEXT)
indx = create_in("./faq_index", faq_schema)


def update_git_repo():
    repo = Repo("./balanced-docs/")
    remote = repo.remote('origin')
    remote.pull()


def faq_processor(path):
    meta = {'tags': []}
    with open(path, 'r') as faq_file:
        data = faq_file.read()
        try:
            section_split = data.split('---')
            top_part = section_split[1]
            bottom_part = section_split[-1]
            for line in top_part.splitlines():
                if line.startswith('title'):
                    meta['title'] = line.split(':')[1].strip()
                if line.startswith('layout'):
                    meta['layout'] = line.split(':')[1].strip()
                if line.startswith('author'):
                    meta['author'] = line.split(':')[1].strip()
                if line.startswith('- '):
                    meta['tags'].append(line.split('- ')[1].strip())
            meta['body'] = bottom_part.strip()
            return meta
        except IndexError:
            print "Warn {} skipped.".format(path)
            return None


def load_faq_woosh():
    indx_writer = indx.writer()
    for file_path in glob2.glob("./balanced-docs/faq/**/*.md"):
        file_data = faq_processor(file_path)
        if file_data:
            indx_writer.add_document(path=unicode(file_path, errors='ignore'),
                                     title=unicode(file_data['title'],
                                                   errors='ignore'),
                                     tags=unicode(','.join(file_data['tags']),
                                                  errors='ignore'),
                                     body=unicode(file_data['body'],
                                                  errors='ignore')
            )
    indx_writer.commit()

def word_stripper(word):
    fixed = word.translate(None, ",!.;?")
    return fixed

def path_to_github(path):
    url = "https://github.com/balanced/balanced-docs/blob/master/faq/"
    url += quote(path.replace('./balanced-docs/faq/', ''), safe="'")
    print url
    var = requests.post('http://git.io/create', data={'url': url})
    url_short = 'http://git.io/' + var.text
    return url_short

def process_query(query_string):
    paths = []
    new = [unicode(word_stripper(each), errors='ignore') for each in
           query_string.split(' ') if len(each) > 3]
    list_of_terms = []
    for word in new:
        for field in ['title', 'tags', 'body']:
            list_of_terms.append(FuzzyTerm(field, word))
            list_of_terms.append(Variations(field, word))
    with indx.searcher() as searcher:
        results = searcher.search(Or(list_of_terms))
        for each in results:
            paths.append(each['path'])
    return [path_to_github(path) for path in paths[0:3]]


def generate_response(query_string):
    msg = "Pinging {} to help with your question. Standby. Ping them again " \
          "if they don't show up soon.".format(
        ON_DUTY)
    links = process_query(query_string)
    if links:
        msg += " Based on your question these links might be helpful: {}"\
            .format(' '.join(links))
    return msg




