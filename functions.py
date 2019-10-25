  # -*- coding: utf-8 -*-

# Telegram
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler, CallbackQueryHandler, RegexHandler, CallbackContext
from telegram.error import (TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError)

# System libraries
from datetime import date, datetime, timedelta
import random
import mysql.connector
import yaml
import logging
import pytz

# config
with open('config/settings.yaml', 'r') as yaml_config:
    config_map = yaml.load(yaml_config)

# Token of your telegram bot that you created from @BotFather, write it on settings.yaml
TOKEN = config_map["token"]
def read_db_conf():
    print("Lettura della configurazione del database")
    global di_db
    conf = open("config/dbconf.yaml", "r")
    doc = yaml.safe_load(conf)
    try:
        di_db = mysql.connector.connect(
            host = doc["db_host"],
            user = doc["db_user"],
            passwd = doc["db_psw" ],
            database = doc["db_name"]
        )
        print("DB connection successfull")
    except:
        print("DB connection error")
    return

def query(sql):
    try:
        global di_db
        cursor = di_db.cursor()
        cursor.execute(sql)
        if not(sql.startswith("SELECT")):
            di_db.commit()
        return cursor
    except mysql.connector.errors.OperationalError:
        print("Connessione MySQL scaduta, riavvio")
        read_db_conf()
        return query(sql)

#
res = ["uno", "due", "tre", "quattro", "cinque", "sei"] #array di prova
def subscribe_course(update: Update, context: CallbackContext): #non è vero... funziona c:
    message_text = "Scegli l\'anno di iscrizione:"
    september = 9
    nYearsButtons = 3
    options = []
    val = 0
    #da fare il controllo sugli argomenti, non ho ben capito come fare con questa nuova signature
    sel = "year_"
    tz = pytz.timezone('Europe/Rome')
    time = datetime.now(tz)
    checkNewYear = datetime(year= time.year, month= september, day= 1)
    checkNewYear=tz.localize(checkNewYear)
    if time > checkNewYear:
      val = 1	
    for x in range(nYearsButtons):
      options.append(str(time.year - (1-val) - x) + "/" + str((time.year + val) - x))
    keyboard = getButton(sel, options,"", 3)
    context.message.reply_text(message_text, reply_markup=InlineKeyboardMarkup(keyboard))

def button_handler(update: Update, context: CallbackContext):
    
    query = context.callback_query
    data = query.data
    if data.startswith('year_'):
      year = data.split('/')
      userChoices = '/' + year[1]
      printOptions(context, userChoices, 'Dipartimenti', 'department_', "Scegli il dipartimento:", 3)
    elif data.startswith('department_'):
      dep = data.split('_')
      userChoices = '/' + dep[1]
      printOptions(context, userChoices, 'Corsi', 'course_', "Scegli il corso:", 3)
    elif data.startswith('course_'):
      course = data.split('_')
      userChoices = course[1].split('/')
      context.callback_query.edit_message_text(userChoices) #a questo punto in userChoices si hanno le tre scelte [corso, dip, anno]

def getButton(sel, options, data, nButRow):
    i = 1
    keyboard = [[]]
    kb = []
    for el in options:
      kb.append(InlineKeyboardButton(el, callback_data= sel + el + data)) 
      if i%nButRow == 0:
        keyboard.append(kb)
        kb = []
      i+=1
    return keyboard 

def printOptions(context, userChoices, tab, sel, msg, nButRow):
    name = []
 """read_db_conf()         
    res = query('SELECT nome FROM ' + tab).fetchall() """ ##qui dovrebbe andare la connessione per prelevare le opzioni
    for data in res:
      name.append(data)
    keyboard = getButton(sel, name, userChoices, nButRow)
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.callback_query.edit_message_text(msg, reply_markup=reply_markup)
                