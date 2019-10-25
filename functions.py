# -*- coding: utf-8 -*-

# Telegram
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler, CallbackQueryHandler, RegexHandler, CallbackContext
from telegram.error import (
    TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError)

# System libraries
from datetime import date, datetime, timedelta
import random
import mysql.connector
import yaml
import logging
import pytz

def read_db_conf():
    print("Lettura della configurazione del database")
    global di_db
    conf = open("config/dbconf.yaml", "r")
    doc = yaml.safe_load(conf)
    try:
        di_db = mysql.connector.connect(
            host=doc["db_host"],
            user=doc["db_user"],
            passwd=doc["db_psw"],
            database=doc["db_name"]
        )
        print("DB connection successfull")
    except:
        print("DB connection error")
    return

def query(sql):
    try:
        global di_db
        cursor = di_db.cursor(dictionary=True)
        cursor.execute(sql)
        if not(sql.startswith("SELECT")):
            di_db.commit()
        return cursor
    except mysql.connector.errors.OperationalError:
        print("Connessione MySQL scaduta, riavvio")
        read_db_conf()
        return query(sql)
    except Exception as e:
        print(e)

def subscribe_course(update: Update, context: CallbackContext):
    printYears(context)

def buttonHandler(update: Update, context: CallbackContext):

    query = context.callback_query
    data = query.data
    print("query data = " + data)

    if data.startswith('year'):
        data = data[:-1]
        year = data.split('=')[1]
        printDepartment(context, year, data)
    elif data.startswith('department'):
        department = (data.split('|')[0]).split('=')[1]
        year       = (data.split('|')[1]).split('=')[1]
        printCdS(context, year, department, data)
    elif data.startswith('cds'):
        cds        = (data.split('|')[0]).split('=')[1]
        #department = (data.split('|')[1]).split('=')[1]
        year       = (data.split('|')[2]).split('=')[1]
        #printCourseYears(context, year, cds, data)

def printYears(context: CallbackContext):
    september = 9
    nYearsButtons = 3
    options = []
    values = []
    val = 0
    tz = pytz.timezone('Europe/Rome')
    time = datetime.now(tz)
    checkNewYear = datetime(year=time.year, month=september, day=1)
    checkNewYear = tz.localize(checkNewYear)
    if time > checkNewYear:
        val = 1
    for x in range(nYearsButtons):
        options.append(str(time.year - (1-val) - x) + "/" + str((time.year + val) - x))
        values.append("year=" + str((time.year + val) - x))
    keyboard = getKeyboard(options, values, "", 3)
    context.message.reply_text("Seleziona l\'anno accademico", reply_markup=InlineKeyboardMarkup(keyboard))

def printDepartment(context, year, data):
    names = []
    values = []
    sql = "SELECT * FROM Dipartimenti WHERE anno_accademico=" + year + ";"
    res = query(sql).fetchall()
    for record in res:
        names.append(record["nome"])
        values.append("department=" + record["id"])
    printKeyboard(context, names, values, data, "Scegli il dipartimento:", 3)

def printCdS(context, year, department, data):
    names = []
    values = []
    sql = "SELECT * FROM `CdS` WHERE id_dipartimento='" + department + "' AND anno_accademico=" + year + ";"
    res = query(sql).fetchall()
    for record in res:
        names.append(record["nome"])
        values.append("cds=" + str(record["id"]))
    printKeyboard(context, names, values, data, "Scegli il corso di studio:", 2)

def printCourseYears(context, year, cds, data):
    names = []
    values = []
    sql = "SELECT DISTINCT anno FROM `Materie` WHERE id_cds='" + cds + "' AND anno_accademico=" + year + ";"
    res = query(sql).fetchall()
    for record in res:
        names.append(str(record["anno"]) + "° anno")
        values.append("course_year=" + str(record["anno"]))
    printKeyboard(context, names, values, data, "Scegli l\'anno della materia:", 3)

def printKeyboard(context, listToPrint, callbackValues, oldData, msg, nButRow):
    keyboard = getKeyboard(listToPrint, callbackValues, oldData, nButRow)
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.callback_query.edit_message_text(msg, reply_markup=reply_markup)

def getKeyboard(options, values, oldData, nButRow):
    i = 1
    keyboard = [[]]
    kb = []
    for element, value in zip(options, values):
        kb.append(InlineKeyboardButton(element, callback_data=value + "|" + oldData))
        if i % nButRow == 0 or i == len(options):
            keyboard.append(kb)
            kb = []
        i += 1
    return keyboard