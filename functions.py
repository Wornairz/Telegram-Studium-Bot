# -*- coding: utf-8 -*-

import settings

# Telegram
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler, CallbackQueryHandler, RegexHandler, CallbackContext
from telegram.error import (
    TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError)

# System libraries
from datetime import date, datetime, timedelta
import random
import requests

# Others
import mysql.connector
import logging
import pytz


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
        settings.read_db_conf()
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
        if data[len(data)-1] is "|":
            data = data[:-1]
        year = data.split('=')[1]
        printDepartment(context, year, data)
    elif data.startswith('department'):
        department = (data.split('|')[0]).split('=')[1]
        year       = (data.split('|')[1]).split('=')[1]
        printCdS(context, year, department, data)
    elif data.startswith('cds'):
        cds        = (data.split('|')[0])[:-2]
        max_anno   = int(((data.split('|')[0]).split('=')[1]).split('_')[1])
        department = (data.split('|')[1])
        year       = (data.split('|')[2])
        data = cds + '|' + department + '|' + year
        printCourseYears(context, max_anno, data)
    elif data.startswith('courseyear'):
        printSemester(context, data)
    elif data.startswith('semester'):
        semester   = (data.split('|')[0]).split('=')[1]
        courseyear = (data.split('|')[1]).split('=')[1]
        cds        = (data.split('|')[2]).split('=')[1]
        department = (data.split('|')[3]).split('=')[1]
        year       = (data.split('|')[4]).split('=')[1]
        printSubject(context, year, department, cds, courseyear, semester)

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

    for dipartimento in settings.dipartimenti:
        if str(dipartimento["anno_accademico"]) == str(year):
            names.append(dipartimento["nome"])
            values.append("department=" + dipartimento["id"])
    printKeyboard(context, names, values, data, "Scegli il dipartimento:", 3)

def getMaxAnno(nome : str):
    if nome.find("LM", 0, len(nome)) is not -1:
        return 2
    else:
        return 3

def printSemester(context, data):
    names = []
    values = []
    for i in range(2):
        names.append(str(i+1) + "° semestre")
        values.append("semester=" + str(i+1))
    printKeyboard(context, names, values, data, "Scegli il semestre:", 2)

def printCdS(context, year, department, data):
    names = []
    values = []
    for corso in settings.cds:
        if str(corso["anno_accademico"]) == str(year) and str(corso["id_dipartimento"]) == str(department):
            max_anno = getMaxAnno(corso["nome"])
            names.append(corso["nome"])
            values.append("cds=" + str(corso["id"]) + "_" + str(max_anno))
    printKeyboard(context, names, values, data, "Scegli il corso di studio:", 2)

def printCourseYears(context, max_anno : int, data : str):
    names = []
    values = []
    for i in range(max_anno):
        names.append(str(i+1) +  "° anno")
        values.append("courseyear=" + str(i+1))
    printKeyboard(context, names, values, data, "Scegli l\'anno della materia:", max_anno)

def printSubject(context, year, department, cds, courseyear, semester):
    names = []
    values = []
    for materia in settings.materie:
        if str(materia["anno_accademico"]) == str(year) and str(materia["id_cds"]) == str(cds):
            if(str(materia["anno"]) == str(courseyear)):
                #if(str(materia["semestre"]) == str(semester)):
                    names.append(materia["nome"])
                    values.append("subject=" + str(materia["codice_corso"]))
    printKeyboard(context, names, values, "", "Scegli la materia:", 1)

def printKeyboard(context, listToPrint, callbackValues, oldData, msg, nButRow):
    keyboard = getKeyboard(listToPrint, callbackValues, oldData, nButRow)
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.callback_query.edit_message_text(msg, reply_markup=reply_markup)

def getKeyboard(options, values, oldData, nButRow):
    i = 1
    keyboard = [[]]
    kb = []
    for element, value in zip(options, values):
        kb.append(InlineKeyboardButton(element, callback_data = value + "|" + oldData))
        if i % nButRow == 0 or i == len(options):
            keyboard.append(kb)
            kb = []
        i += 1
    # TODO Bottone torna indietro
    #if oldData is not "":
        #keyboard.append([InlineKeyboardButton("Torna indietro", callback_data = oldData)])
    return keyboard