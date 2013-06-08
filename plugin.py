from jeeves.core.plugin import GenericPlugin, CommandPlugin
from app import *


class FaqPluginReq(GenericPlugin):
    name = 'FaqBot'
    help_text = 'Just trying to help'

    def __init__(self, *args, **kwargs):
        load_faq_woosh()
        super(FaqPluginReq, self).__init__(self.name, *args, **kwargs)

    def handle_message(self, channel, nickname, message):
        if 'q' in message:
            new_mesasge = message.replace('q', '')
            response = generate_response(new_mesasge)
            self.say(channel, response)
