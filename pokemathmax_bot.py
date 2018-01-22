#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""
__date__ = "Created on Sat Jan 20 16:48:45 2018"
__version__ = "0.1.0"
__author = "Qu Dong"
import crawler.pokerequests as pokemaxcrawler
from wheel.color import *

TOKEN = "529317767:AAHhQFXGU3Bu55Ce4Kbv3C0Sf7XtvnsbXwo"


# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Introduction-to-the-API
import telegram
bot = telegram.Bot(token=TOKEN)
a = bot.get_me()



# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-Your-first-Bot
from telegram.ext import Updater
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def start(bot, update):
    loco = (1.447501, 103.812063)
    colorprint("Current location is ({}, {})".format(*loco), color="cyan")
    radius_all = 500
    pkms = pokemaxcrawler.get_nearby_pkm_obj_list(current_lat_lng=loco,
                                              radius=radius_all)
    pkm_str = '\n\n'.join(str(x) for x in pkms)
    bot.send_message(chat_id=update.message.chat_id, text=pkm_str)
    
    
from telegram.ext import CommandHandler
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()

#def echo(bot, update):
#    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)
#
#from telegram.ext import MessageHandler, Filters
#echo_handler = MessageHandler(Filters.text, echo)
#dispatcher.add_handler(echo_handler)
#
#def caps(bot, update, args):
#    text_caps = ' '.join(args).upper()
#    bot.send_message(chat_id=update.message.chat_id, text=text_caps)
#
#caps_handler = CommandHandler('caps', caps, pass_args=True)
#dispatcher.add_handler(caps_handler)