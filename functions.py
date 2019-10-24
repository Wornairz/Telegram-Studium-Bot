# -*- coding: utf-8 -*-

# Telegram
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler, CallbackQueryHandler, RegexHandler
from telegram.error import (TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError)

# System libraries
from datetime import date, datetime, timedelta
import datetime
import random
#import os
#import sys
#import requests
import sqlite3
import yaml
import logging
#from urllib.request import urlopen
#from bs4 import BeautifulSoup

# config
with open('config/settings.yaml', 'r') as yaml_config:
    config_map = yaml.load(yaml_config)

# Token of your telegram bot that you created from @BotFather, write it on settings.yaml
TOKEN = config_map["token"]

def print_cds(bot, update, args, dip):
    anno = args[0]

    if(not args):
        anno = "2020"
        bot.sendMessage(chat_id = update.message.chat_id, text = "Nessun anno inserito (default anno accademico 2019/2020)")

    conn = sqlite3.connect('data/Studium_DB.db')
    cds = conn.execute("SELECT * FROM CDS WHERE Anno = " + str(anno) + " AND dip = " + str(dip) + ";")

    message = ""

    for c in cds:
        message += c[0] + " " + c[1] + " " + c[4] + "\n"

    bot.sendMessage(chat_id = update.message.chat_id, text = message)
    conn.close()

def print_dip(bot, update, args):
    anno = args[0]

    if(not args):
        anno = "2020"
        bot.sendMessage(chat_id = update.message.chat_id, text = "Nessun anno inserito (default anno accademico 2019/2020)")

    conn = sqlite3.connect('data/Studium_DB.db')
    dipartimenti = conn.execute("SELECT * FROM Dipartimenti WHERE Anno = " + anno)

    message = ""

    for d in dipartimenti:
        message += d[0] + " " + d[1] + " " + d[4] + "\n"

    bot.sendMessage(chat_id = update.message.chat_id, text = message)
    conn.close()

def print_courses(bot, update, args, cds):
    anno = args[0]

    if(not args):
        anno = "2020"
        bot.sendMessage(chat_id = update.message.chat_id, text = "Nessun anno inserito (default anno accademico 2019/2020)")

    conn = sqlite3.connect('data/Studium_DB.db')
    materie = conn.execute("SELECT * FROM Materie WHERE Anno = " + anno + " AND cds = " + str(cds) + ";")

    message = ""

    for m in materie:
        message += m[0] + " " + m[1] + " " + m[4] + "\n"

    bot.sendMessage(chat_id = update.message.chat_id, text = message)
    conn.close()

def subscribe_course(bot, update, args):

    if(not args):
        bot.sendMessage(chat_id = update.message.chat_id, text = "Nessun codice corso inserito")
        return
        
    conn = sqlite3.connect('data/Studium_DB.db')
    chat_id = update.message.chat_id
    username = update.message.from_user.username
    anno_iscrizione = 2020  #Soluzione temporanea
    codice_corso = args[0]

    if(conn.execute("SELECT Chat_id FROM 'Utenti' WHERE Chat_id = " + str(chat_id)).fetchone() is None):
        conn.execute("INSERT INTO 'Utenti' VALUES(" \
        + str(chat_id) + ",'"   \
        + str(username) + "')")

    try:
        conn.execute("INSERT INTO 'Iscrizioni' VALUES(" \
        + str(chat_id) + "," \
        + str(codice_corso) + "," \
        + str(anno_iscrizione) + "," \
        + ")")
    except:
        bot.sendMessage(chat_id = chat_id, text = "Sei già iscritto a questo corso!")

    conn.close()
