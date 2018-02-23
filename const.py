# -*- coding: utf-8 -*-

import gettext
gettext.install('const', './lang')

INVITE_CATEGORY =_('''
        Choose the category
        ''')
INVITE_SUBCATEGORY = _('''
        Choose the subcategory
        ''')
SMTH_WRONG = _('''
        Something go bad
        Now we will fix everything; \
        try again later or choose another service!
        ''')

superusers = [] #!

SC_IS_EMPTY = _('''
        There are no companies in this subcategory yet
        You can choose other service
        ''')
NO_CATEGORY=_('''
        We haven't such category yet
        But you have an access to all the other!
        ''')
NO_SUBCATEGORY=_('''
        We haven't such subcategory yet
        But you have an access to all the other!
        ''')

UNIQUE_USERS = _("Number of unique users: %d\n")
UNIQUE_CLICKS = _("Number of unique clicks on all bots: %d")

FAQ = _('''
    Command list:
    /start - back to choosing categories
    ''')

WEBHOOK_HOST = '194.87.0.0'
WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port has to be open!)
WEBHOOK_LISTEN = '194.87.0.0'  # On some servers we have to use the same IP with higher

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # The way to cerficate
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # The way to private key

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
