# -*- coding: utf-8 -*-

# Telegram
from telegram import Update
from telegram.ext import CallbackContext

# System libraries

# Module
from Modules.Keyboard import *
import settings

# Others

def confirm_unsubscription(chat_id, codice_corso, context, data):
    settings.query("DELETE FROM Iscrizioni WHERE chat_id=" + str(chat_id) + " AND codice_corso=" + str(codice_corso))
    printConfirmedUnsubscription(context)

def printUnsubscribe(context: CallbackContext):
    names = []
    values = []
    chat_id = context.callback_query.message.chat_id
    print("prova")
    for subject in subscribed_subject(chat_id):
        names.append("📚 " + str(subject.split("|")[0]))
        values.append("dis=" + str(subject.split("|")[1]))
    if not names:
        context.callback_query.edit_message_text("Non sei iscritto a nessun corso, se vuoi iscriverti lancia il comando /studium")
    else:
        printKeyboard(context, names, values, "", "Seleziona la materia da cui vuoi disiscriverti", 1)

def subscribed_subject(chat_id):
    subscribedSubject = []
    res = settings.query("SELECT * FROM Iscrizioni WHERE chat_id=" + str(chat_id))
    for record in res:
        for materia in settings.materie:
            if record["codice_corso"] == materia["codice_corso"]:
                subscribedSubject.append(str(materia["nome"]) + "|" + str(materia["codice_corso"]))
    return subscribedSubject

def printChoiceUnSubscription(context, subject, oldData):
    keyboard = [[InlineKeyboardButton("✅ Sì", callback_data = "confDis" + "|" + oldData),
                 InlineKeyboardButton("🔙 Indietro", callback_data = "reload_dis")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    name = ""
    for materia in settings.materie:
        if str(materia["codice_corso"]) == str(subject):
            name = materia["nome"]
    context.callback_query.edit_message_text("Vuoi discriverti a " + name + "?", reply_markup=reply_markup)

def printConfirmedUnsubscription(context):
    context.callback_query.edit_message_text("Discrizione avvenuta con successo!")



