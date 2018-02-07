# -*- coding: utf-8 -*-
import const
import telebot
from telebot import types
import sqlite3
from datetime import datetime
import cherrypy
from const import WEBHOOK_HOST, WEBHOOK_PORT, WEBHOOK_LISTEN, \
                  WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV, \
                  WEBHOOK_URL_BASE
import sys
import logging
import urllib3
import tokens

bot = telebot.TeleBot(tokens.token_main)

reply = "null"
logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG,
                    filename=u'YourSupportLogs.log')


categories = []


def load_categories():
    """
    Return list of categories from DB

    """
    print("Loading categories...")
    con = sqlite3.connect('test.db')
    cur = con.cursor()
    cur.execute('SELECT name FROM categories')
    categories_ = cur.fetchall()


    #print("Loading superusers...")
    #cur.execute('SELECT chat_id FROM superusers')
    #users = cur.fetchall()
    #con.close()
    #for x in users:
        #superusers.append(int(x[0]))

    for n in categories_:
        categories.append(n[0])

    WEBHOOK_URL_PATH = "/%s/" % tokens.token_main

load_categories()#!!!


def check_users(cur_id):
    print("Checking users...")
    con = sqlite3.connect('test.db')
    cur = con.cursor()
    cur.execute('SELECT user_id FROM users')
    all_users_ = cur.fetchall()
    all_ussers = [int(x[0]) for x in all_users_]
    if not cur_id in all_ussers:
        cur.execute("INSERT INTO 'users' ('user_id') VALUES (%d)" % cur_id)
        con.commit()
    con.close()


def get_visit_counts():
    print("Loading visits...")
    con = sqlite3.connect('test.db')
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM users")
    users_count = int(cur.fetchone()[0])
    cur.execute("SELECT DISTINCT telegram FROM companies")
    telegrams_ = cur.fetchall()
    con.close()
    telegrams = [str(x[0]) for x in telegrams_]
    http = urllib3.PoolManager()
    clicks_count = 0
    for t_name in telegrams:
        response = http.request('GET',
                                'https://beautyhttp.herokuapp.com/get_counter/%s/' % t_name)
        clicks_count += int(response.data)
    return [users_count, clicks_count]

code_wrongs = {
    -1: const.smth_wrong,
    1: const.sc_is_empty,
    2: const.no_category,
    3: const.no_subcategory
}

"""WEBHOOK CLASS"""

class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                'content-type' in cherrypy.request.headers and \
                cherrypy.request.headers['content-type'] == 'application/json':

            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)

"""END WEBHOOK CLASS. BELOW JUST YOUR CODE"""


@bot.message_handler(commands=["get"])
def get_statistics(m):
    """
        To know your chat_id
    """
    print(str(m.chat.id))
    if m.chat.id in const.superusers:
        print("superuser")
        counts = get_visit_counts()
        print(str(counts))
        bot.send_message(m.chat.id, "Количество уникальных пользователей: %d\n"
                                    "Количество уникальных кликов по всем ботам: %d" % (
                             counts[0], counts[1]))

@bot.message_handler(commands=['start'])
def start(m):
    """
    Some actions with server
    User will see buttons-categories
    Transfer control to choose_category (next handler)
    """

    print("Start command")
    check_users(m.chat.id)

    #http = urllib3.PoolManager()
    #http.request('GET', 'https://beautyhttp.herokuapp.com', timeout=0.5)
    #keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=2)
    print("start2")
    msg = invalidate(m, const.invite_cat, categories)
    bot.register_next_step_handler(msg, choose_category)

def invalidate(m, text_mes, list):
    """
    Show a grid of buttons, which associated with elements of list

    """
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(*[types.KeyboardButton(n) for n in list])
    msg = bot.send_message(m.chat.id, text_mes, reply_markup=keyboard)
    return msg

def choose_category(m):
    """
    User will see buttons-subcategories
    Transfer control to choose_subcategory (next handler)

    """
    i = 1
    print("category")
    for name in categories:
        if m.text == name and i == len(categories):
            bot.send_message(m.chat.id, const.FAQ)
            msg = invalidate(m, const.invite_cat, categories)
            bot.register_next_step_handler(msg, choose_category)
            return  # handling of FAQ
        if m.text == name and i < len(categories):
            sc = load_subcategories(i + 1)
            if (sc == -1):
                execuse_smth(m, code=-1)
                return
            if (sc == []):
                execuse_smth(m, code=0)
                return
            msg = invalidate(m, const.invite_sc, sc)
            bot.register_next_step_handler(msg, choose_subcategory)
            return
        i += 1

    if not m.text in const.available_commands:
        execuse_smth(m, code=2)
    return

def load_subcategories(number_cat):
    """
    Load names of subcategories from DB after choosing category

    """
    try:
        con = sqlite3.connect('test.db')
        cur = con.cursor()
        cur.execute('SELECT name FROM subcategories WHERE main_category_id = (?)', (number_cat,))
        subcategories = cur.fetchall()
        i = 0
        for n in subcategories:
            subcategories[i] = n[0]
            i += 1
        # print("suc")
        con.close()
    except Exception as e:
        subcategories = -1
        handling_error(e)

    return subcategories

def choose_subcategory(m):
    """
    User will see info about companies
    Transfer control to choose_category

    """
    print("subcategory")
    if m.text in const.available_commands:
        return None

    id = get_subcategory_id(m.text)
    # print(id)
    # print(m.text)
    # print(const.available_commands)
    if id == -1:
        execuse_smth(m, code=3)
        return None

    list_of_companies = get_company_info(1)
    # !! list_of_companies = get_company_info(id)

    if not list_of_companies:
        execuse_smth(m, code=1)
        return None

    for company in list_of_companies:
        keyboard = types.InlineKeyboardMarkup()
        text_url = "https://beautyhttp.herokuapp.com/redirect_user/"
        text_url += str(m.chat.id) + "/"
        text_url += company[5] + "/"
        # print(text_url)
        url_button = types.InlineKeyboardButton(
            text="telegram канал", url=text_url)
        keyboard.add(url_button)
        bot.send_message(m.chat.id, company_out_text(company), reply_markup=keyboard)

    msg = invalidate(m, const.invite_cat, categories)
    bot.register_next_step_handler(msg, choose_category)
    return None

def get_subcategory_id(name):
    """
    Return id of choossing subcategory
    """
    try:
        con = sqlite3.connect('test.db')
        cur = con.cursor()
        # print(name)
        cur.execute('SELECT subcategory_id FROM subcategories WHERE name = (?)', [name])
        res = cur.fetchall()
        con.close()
        # print(res)
        if not res:
            return -1
        return res[0][0]

    except Exception as e:
        res = -1
        handling_error(e)
        return res

def get_company_info(number_sc):
    """
    Return a list of companies which belongs definite subcategory

    """
    con = sqlite3.connect('test.db')  # do try
    cur = con.cursor()
    cur.execute('SELECT * FROM companies WHERE main_subcategory_id = (?)', [number_sc])
    res = cur.fetchall()
    con.close()
    return res

def company_out_text(text):
    """
     Return description of company

    """
    out_t = text[2] + "\n"  # name
    out_t += text[3] + "\n"  # description
    out_t += "Рабочий телефон \n" + text[4]
    return out_t

def handling_error(e):
    """
    Report developers about problems

    """
    # print(e)
    bot.send_message(const.my_chat, e)
    t = datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")
    f = open('errors.txt', 'a')
    text = str(e) + '\n' + t + '\n'
    f.write(text)
    f.close()
    bot.send_message(const.my_chat, t)

def execuse_smth(m, code):
    """
    Report user about problem
    Transfer control to choose_category (next handler)

    """
    text = code_wrongs[code]
    bot.send_message(m.chat.id, text)
    msg = invalidate(m, const.invite_cat, categories)
    bot.register_next_step_handler(msg, choose_category)
    return


"""WEBHOOKS SET UP:"""  # please make class because I want to roll up it. OK, I heared you!! ;-)
                        #  But I have to replace all this shitcode
if len(sys.argv) > 1 and sys.argv[1] == 'deploy':
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                    certificate=open(WEBHOOK_SSL_CERT, 'r'))

    cherrypy.config.update({
        'server.socket_host': WEBHOOK_LISTEN,
        'server.socket_port': WEBHOOK_PORT,
        'server.ssl_module': 'builtin',
        'server.ssl_certificate': WEBHOOK_SSL_CERT,
        'server.ssl_private_key': WEBHOOK_SSL_PRIV
    })

if len(sys.argv) < 2:
    print("Specify starting mode [dev, deploy]")
else:
    if sys.argv[1] == 'deploy':
        cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})
    elif sys.argv[1] == 'dev':
        '''
        main action
        '''

        bot.remove_webhook()
        if __name__ == '__main__':
            bot.polling(none_stop=True)
    else:
        print("Specify starting mode [dev, deploy]")