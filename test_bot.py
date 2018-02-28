# -*- coding: utf-8 -*-

import config
import cherrypy
import telebot
import tokens

test_bot = telebot.TeleBot(tokens.test_token)

@test_bot.message_handler(content_types=["text"])
def send_message(message):
        test_bot.send_message(message.chat.id, message.text)

class WebhookServer(object):
    @cherrypy.expose
    def index(self):
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            test_bot.process_new_updates([update])
            return ''

if __name__ == '__main__':
    """
    WEBHOOK SET UP:

    """
    cherrypy.config.update({
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 7001,
        'engine.autoreload.on': False
    })
    cherrypy.quickstart(WebhookServer(), '/', {'/': {}})
