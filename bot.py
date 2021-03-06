# -*- coding: utf-8 -*-

import sys
import logging
import urllib3
from datetime import datetime

import telebot
from telebot import types
import sqlite3
import cherrypy

from classSC import *
from const import *
from config import *
from webhook import WebhookServer
from webhook import bot


categories = []
categories_id = []
subcategories = []

code_wrongs = {
    -1: SMTH_WRONG,
    1: SC_IS_EMPTY,
    2: NO_CATEGORY,
    3: NO_SUBCATEGORY
}

def main():
    load_categories()
    load_subcategories()
    logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s',
                        level=logging.DEBUG, filename=u'YourSupportLogs.log')#!
    bot.remove_webhook()
    if ((len(sys.argv) < 2) or
            ((sys.argv[1] != 'dev') and (sys.argv[1] != 'deploy'))):
        print("Specify starting mode (first arg) 'dev' or 'deploy'")
        sys.exit()

    if(sys.argv[1] == 'deploy'):
        deploy()
    if(sys.argv[1] == 'dev'):
        bot.polling(none_stop=True)

def load_categories():
    """
    Load Category objects from DB

    """
    print("Loading categories...")
    connectorDB = sqlite3.connect('test.db')
    cursorDB = connectorDB.cursor()
    cursorDB.execute('SELECT * FROM categories')
    categories_ = cursorDB.fetchall()
    connectorDB.close()
    for n in categories_:
        categories.append(n[1])
        categories_id.append(n[0])
    return

def load_subcategories():
    """
    Load Subcategory objects from DB

    """
    connectorDB = sqlite3.connect('test.db')
    cursorDB = connectorDB.cursor()
    cursorDB.execute('SELECT * FROM subcategories')
    subcategories_ = cursorDB.fetchall()
    connectorDB.close()
    i = 0
    for n in subcategories_:
        sc = Subcategory(n[1], n[2], n[0])
        subcategories.append(sc)
    return

@bot.message_handler(commands=["get"])
def get_statistics(message):
    """
        To know your chat_id
    """
    print(str(message.chat.id))
    if m.chat.id in superusers:
        counts = get_visit_counts()
        print(str(counts))
        bot.send_message(m.chat.id, UNIQUE_USERS, UNIQUE_CLICKS  % ( ##
                             counts[0], counts[1]))

@bot.message_handler(commands=["start"])
def start(message):
    """
    Some actions with server
    User will see buttons-categories

    """
    print("Start command")
    check_users(message.chat.id)
    msg = invalidate(message, INVITE_CATEGORY, categories)#start_const

@bot.message_handler(content_types=["text"])
def user_send_text(message):
    """
    User send message, check if it' s a category -> show subcategories
                                      a subcategory -> show companies

    """
    categoryID = check_categories(message.text)
    if(categoryID != 0):
        currentSubcategories = choose_subcategory(categoryID)
        msg = invalidate(message, INVITE_SUBCATEGORY,
                        currentSubcategories, buttonBack = 1)
        return
    subcategoryID = check_subcategories(message.text)
    if(subcategoryID != 0):
         show_companies_in_subcategory(message, subcategoryID)
         msg = invalidate(message, INVITE_CATEGORY, categories)
         return

    if(message.text == BACK):
        msg = invalidate(message, INVITE_CATEGORY, categories)
        return
    msg = invalidate(message, INVITE_CATEGORY, categories)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "class":
        bot.send_message(call.message.chat.id, "class")
    if call.data == "not_class":
        bot.send_message(call.message.chat.id, "not_class")


def check_categories(text):
    """
    Return id of choosen category, if there' s no such category -> 0

    """
    i = 0 #
    for c in categories:
        if(c == text):
            return categories_id[i]
        i = i+1
    return 0

def choose_subcategory(id):
    """
    Return list of names subcategories, which belong to category with id

    """
    currentSubcategories = []
    for sc in subcategories:
        if(sc.check_mainID(id)):
            currentSubcategories.append(sc.get_name())
    return currentSubcategories

def check_subcategories(text):
    """
    Return id of choosen subcategory, if there' s no such subcategory -> 0

    """
    for sc in subcategories:
        if(sc.check_name(text) == True):
            return(sc.get_id())
    return 0

def invalidate(m, text_mes, list, buttonBack=0):
    """
    Show a grid of buttons, which associated with elements of list

    """
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2,
                                        one_time_keyboard = True)
    keyboard.add(*[types.KeyboardButton(n) for n in list])
    if buttonBack == 1:
    	keyboard.add(types.KeyboardButton(BACK))
    msg = bot.send_message(m.chat.id, text_mes, reply_markup=keyboard)
    return msg

def show_companies_in_subcategory(message, subcategoryID):
    """
    User will see info about companies

    """
    list_of_companies = get_company_info(subcategoryID)
    if not list_of_companies:
        execuse_smth(message, code=1) ##
        return None
    for company in list_of_companies:
        """
        keyboard = types.InlineKeyboardMarkup()
        text_url = "https://beautyhttp.herokuapp.com/redirect_user/"
        text_url += str(m.chat.id) + "/"
        text_url += company[5] + "/"
        # print(text_url)
        url_button = types.InlineKeyboardButton(
            text="telegram канал", url=text_url)
        keyboard.add(url_button)
        """
        keyboard = types.InlineKeyboardMarkup(row_width = 2)
        callback_button_1 = types.InlineKeyboardButton(text="class",
                                                     callback_data="class")
        callback_button_2 = types.InlineKeyboardButton(text="not_class",
                                                     callback_data="not_class")
        keyboard.add(callback_button_1,callback_button_2)
        bot.send_message(message.chat.id, company_out_text(company),reply_markup=keyboard)
        #bot.send_message(message.chat.id, "lol",reply_markup=keyboard)

def check_users(cur_id):
    print("Checking users...")
    connectorDB = sqlite3.connect('test.db')
    cursorDB = connectorDB.cursor()
    cursorDB.execute('SELECT user_id FROM users')
    all_users_ = cursorDB.fetchall()
    all_ussers = [int(x[0]) for x in all_users_]
    if not cur_id in all_ussers:
        cursorDB.execute("INSERT INTO 'users' ('user_id') VALUES (%d)" % cur_id)
        connectorDB.commit()
    connectorDB.close()

def get_visit_counts():
    print("Loading visits...")
    connectorDB = sqlite3.connect('test.db')
    cursorDB = connectorDB.cursor()
    cursorDB.execute("SELECT COUNT(*) FROM users")
    users_count = int(cursorDB.fetchone()[0])
    cursorDB.execute("SELECT DISTINCT telegram FROM companies")
    telegrams_ = cursorDB.fetchall()
    connectorDB.close()
    telegrams = [str(x[0]) for x in telegrams_]
    http = urllib3.PoolManager()
    clicks_count = 0
    for t_name in telegrams:
        response = http.request('GET',
                                'https://beautyhttp.herokuapp.com/get_counter/%s/' % t_name)
        clicks_count += int(response.data)
    return [users_count, clicks_count]

def get_company_info(number_sc):
    """
    Return a list of companies which belongs definite subcategory

    """
    connectorDB = sqlite3.connect('test.db')  # do try
    cursorDB = connectorDB.cursor()
    cursorDB.execute('SELECT * FROM companies WHERE main_subcategory_id = (?)', [number_sc])
    res = cursorDB.fetchall()
    connectorDB.close()
    return res

def company_out_text(text):
    """
     Return description of company

    """
    out_t = text[2] + "\n"  # name
    out_t += text[3] + "\n"  # description
    out_t += "Рабочий телефон \n" + text[4] + "\n"
    out_t += "@your_support_bot"
    return out_t

def handling_error(e):
    """
    Report developers about problems

    """
    # print(e)
    bot.send_message(my_chat, e)
    t = datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M:%S")
    f = open('errors.txt', 'a')
    text = str(e) + '\n' + t + '\n'
    f.write(text)
    f.close()
    bot.send_message(my_chat, t)

def execuse_smth(message, code):
    """
    Report user about problem

    """
    text = code_wrongs[code]
    bot.send_message(message.chat.id, text)
    return

def deploy():
    """
    WEBHOOK SET UP:

    """
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL_BASE + MAIN_BOT_UPDATE,
                    certificate=open(WEBHOOK_SSL_CERT, 'r'))
    cherrypy.config.update({
        'server.socket_host': '127.0.0.1',
        'server.socket_port': MAIN_BOT_PORT,
        'engine.autoreload.on': False
    })
    cherrypy.quickstart(WebhookServer(), '/', {'/': {}})

if __name__ == '__main__':
    main();
