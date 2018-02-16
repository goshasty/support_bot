# -*- coding: utf-8 -*-

import gettext
gettext.install('const', './lang')

invite_cat =_('''
        Choose the category
        ''')
invite_sc = _('''
        Choose the subcategory
        ''')
smth_wrong = _('''
        Something go bad
        Now we will fix everything; \
        try again later or choose other service!
        ''')
my_chat = 254282848


superusers = [my_chat,] #!

sc_is_empty = _('''
        There are no companies in this subcategory yet
        You can choose other service
        ''')
no_category=_('''
        We haven't such category yet
        But you have an access to all the other!
        ''')
no_subcategory=_('''
        We haven't such subcategory yet
        But you have an access to all the other!
        ''')

unique_users = _("Number of unique users: %d\n")
unique_clicks = _("Number of unique clicks on all bots: %d")

back = "⇐ back"

FAQ = _('''
    Command list:
    /start - back to choosing categories
    ''')
available_commands = ("/start", "/get")



WEBHOOK_HOST = '194.87.0.0'
WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port has to be open!)
WEBHOOK_LISTEN = '194.87.0.0'  # On some servers we have to use the same IP with higher

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # The way to cerficate
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # The way to private key

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
