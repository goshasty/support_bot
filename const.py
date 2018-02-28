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
        Now we will fix everythinng; \
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

BACK = "<<"

UNIQUE_USERS = _("Number of unique users: %d\n")
UNIQUE_CLICKS = _("Number of unique clicks on all bots: %d")

FAQ = _('''
    Command list:
    /start - back to choosing categories
    ''')

