
import cherrypy
import telebot
from config import MAIN_BOT_TOKEN

bot = telebot.TeleBot(MAIN_BOT_TOKEN)

class WebhookServer(object):
    @cherrypy.expose
    def index(self):
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return ''
