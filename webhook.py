# -*- coding: utf-8 -*-

import config
import cherrypy
import telebot
import tokens
import requests

bot = telebot.TeleBot(tokens.token)
test_bot = telebot.TeleBot(tokens.test_token)

class WebhookServer(object):
    @cherrypy.expose
    def bot_update(self):
        if 'content-length' in cherrypy.request.headers and \
            'content-type' in cherrypy.request.headers and \
            cherrypy.request.headers['content-type'] == 'application/json':

            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            requests.post(config.MAIN_BOT_ADDRESS, data=json_string)
            return ''
        else:
            raise cherrypy.HTTPError(403)

    @cherrypy.expose
    def test_bot_update(self):
        if 'content-length' in cherrypy.request.headers and \
            'content-type' in cherrypy.request.headers and \
            cherrypy.request.headers['content-type'] == 'application/json':

            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            requests.post(config.TEST_BOT_ADDRESS, data=json_string)
            return ''
        else:
            raise cherrypy.HTTPError(403)

if __name__ == '__main__':
    """
    WEBHOOKS SET UP:
        
    """
    bot.remove_webhook()
    bot.set_webhook(url=config.WEBHOOK_URL_BASE + '/bot_update',
                    certificate=open(config.WEBHOOK_SSL_CERT, 'r'))

    test_bot.remove_webhook()
    test_bot.set_webhook(url=config.WEBHOOK_URL_BASE + '/test_bot_update',
                    certificate=open(config.WEBHOOK_SSL_CERT, 'r'))

    cherrypy.config.update({
        'server.socket_host': config.WEBHOOK_LISTEN,
        'server.socket_port': config.WEBHOOK_PORT,
        'server.ssl_module': 'builtin',
        'server.ssl_certificate': config.WEBHOOK_SSL_CERT,
        'server.ssl_private_key': config.WEBHOOK_SSL_PRIV,
        'engine.autoreload.on': False
    })
    cherrypy.quickstart(WebhookServer(), '/', {'/': {}})
