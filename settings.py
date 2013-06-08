# Jeeves settings


HOST = 'irc.freenode.net'
PORT = 6667  # 6697 for SSL
SSL = False
SERVER_PASSWORD = None
PASSWORD = 'BalBot1212'
NICKNAME = 'BalBot'
REALNAME = 'The beastly balanced Bot'
ON_DUTY = 'PN-Balanced'
CHANNEL = '#testing12345'

PLUGINS = (
    #It is strongly recommended that you don't remove these (jeeves.core.plugins.*) plugins
    #'jeeves.core.plugins.admin.HelpPlugin',

    #Optional Jeeves Plugins. Uncomment any you'd like to use.
    #'jeeves.contrib.plugins.ticketbot.TicketBotPlugin',
    #'jeeves.contrib.plugins.shortener.ShortenPlugin',

    #Here you can add any of the plugins that you create.
    'plugin.FaqPluginReq',
    #'plugins.example.ExampleCommandPlugin',
)

"""
###########################
# Shorten Plugin Settings #
###########################
# Backend shortening service. Defaults to google
SHORTENER_BACKEND = 'google'
# Login account. Defaults to None
SHORTENER_LOGIN = None
# API Key. Defaults to None
SHORTENER_API_KEY = None
"""

"""
#############################
# TicketBot Plugin Settings #
#############################
TICKETBOT_TICKET_URL = None  # Example: 'https://github.com/silent1mezzo/jeeves-framework/issues/%s'
TICKETBOT_CHANGESET_URL = None  # Example: 'https://github.com/silent1mezzo/jeeves-framework/commit/%s'
"""
