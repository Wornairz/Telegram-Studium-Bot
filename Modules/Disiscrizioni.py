# -*- coding: utf-8 -*-

# Telegram
from telegram import Update
from telegram.ext import CallbackContext

# System libraries

# Module
from Modules.Keyboard import *
import settings

# Others

def confirm_unsubscription(chat_id, codice_corso, update, context, data):
    settings.query("DELETE FROM Iscrizioni WHERE chat_id=" + str(chat_id) + " AND codice_corso=" + str(codice_corso))
    printConfirmedUnsubscription(update, context)

def printUnsubscribe(update: Update, context: CallbackContext, first_time = True):
    names = []
    values = []
    chat_id = update.message.chat_id if first_time else update.callback_query.message.chat_id
    for subject in subscribed_subject(chat_id):
        names.append("📕 " + str(subject.split("|")[0]))
        values.append("dis=" + str(subject.split("|")[1]))
    if not names:
        update.message.reply_text("Non sei iscritto a nessun corso, se vuoi iscriverti clicca sul bottone nella tastiera.")
    else:
        printKeyboard(update, context, names, values, "", "Seleziona la materia da cui vuoi disiscriverti:", 1, reply= first_time)

def subscribed_subject(chat_id):
    subscribedSubject = []
    res = settings.query("SELECT * FROM Iscrizioni WHERE chat_id=" + str(chat_id))
    for record in res:
        for materia in settings.materie:
            if record["codice_corso"] == materia["id"]:
                subscribedSubject.append(str(materia["name"]) + "|" + str(materia["id"]))
    return subscribedSubject

def printChoiceUnSubscription(update, context, subject, oldData):
    keyboard = [[InlineKeyboardButton("✅ Sì", callback_data = "confDis" + "|" + oldData),
                 InlineKeyboardButton("🔙 Indietro", callback_data = "reload_dis")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    name = ""
    for materia in settings.materie:
        if str(materia["id"]) == str(subject):
            name = materia["name"]
    update.callback_query.edit_message_text("Vuoi discriverti a " + name + "?", reply_markup=reply_markup)

def printConfirmedUnsubscription(update, context):
    update.callback_query.edit_message_text("Discrizione avvenuta con successo!")



