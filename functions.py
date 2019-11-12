# -*- coding: utf-8 -*-

# Telegram
import telegram
from telegram import Update

# System libraries

# Module
from Modules.Iscrizioni import *
from Modules.Disiscrizioni import *
from Modules.Keyboard import *

# Others

def getHelp(update: Update, context: CallbackContext):
    msg= "Seleziona uno dei seguenti bottoni:\n\n"
    msg+= "✅ Iscriviti - usalo per iscriverti ai corsi che ti interessano;\n"
    msg+= "❌ Disiscriviti - ti permette di disiscriverti da uno dei corsi al quale sei iscritto;\n"
    msg+= "📚 Mie iscrizioni - mostra una lista delle tue attuali iscrizioni;\n\n"
    msg += "Se dovesse sparire il menù nella tastiera, digita /studium."
    context.bot.sendMessage(chat_id= update.message.chat_id, text= msg)

def startingBot(update: Update, context: CallbackContext):
    msg = "Ciao! Benvenuto in Studium Bot 😃, il bot che ti permette di ricevere gli avvisi dei tuoi corsi qui su telegram.\n"
    msg += "Per iniziare ad iscriverti al tuo primo corso, seleziona il bottone Iscriviti giù nella tastiera."
    printMenu(update, context, msg)

def studiumMenu(update: Update, context: CallbackContext):
    msg = "Seleziona giù nella tastiera un'azione da intraprendere."
    printMenu(update, context, msg)

def getSubjectName(id):
    for materia in settings.materie:
        if str(materia["codice_corso"]) == str(id):
            return str(materia["nome"])
    return -1

def forwardNotices(context: CallbackContext):
    avvisi_json = settings.read_remote_avvisi()
    for avviso in avvisi_json:
        nome_materia = getSubjectName(avviso["idSubject"])
        msg = "<b>" + str(nome_materia) + "</b>\n\n"
        msg += "<b>Professore</b>: " + str(avviso["teacher"]) + "\n"
        msg += "<b>Titolo</b>: " + str(avviso["title"]) + "\n\n"
        msg += "<b>Testo</b>: \n" + str(avviso["text"]) + "\n\n"
        msg += "<b>Data</b>: " + str(avviso["date"])
        iscritti = settings.query("SELECT chat_id FROM Iscrizioni WHERE codice_corso=" + str(avviso["idSubject"]))
        for iscritto in iscritti:
            context.bot.sendMessage(chat_id=iscritto["chat_id"], text=msg, parse_mode=telegram.ParseMode.HTML)

def subscribed_subject_text_list(update: Update, context: CallbackContext):
    msg = ""
    for subject in subscribed_subject(update.message.chat_id):
        msg += "✅  " + subject.split("|")[0] + "\n\n"
    if msg is "":
        msg = "Non sei iscritto a nessun corso, se vuoi iscriverti clicca sul bottone nella tastiera"
    update.message.reply_text(msg)

def studium_menu(update: Update, context: CallbackContext):
    menu = ["✅ Iscriviti", "❌ Disiscriviti", "📚 Mie iscrizioni"]
    callback_menu = ["iscriviti", "disiscriviti", "mie_iscrizioni"]
    printKeyboard(update, context, menu, callback_menu, "", "Scegli una operazione da effettuare: ", 1, reply=True)

def buttonHandler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    #print("query data = " + data)
    if data == "Esc":
        chat_id = update.callback_query.message.chat_id
        message_id = update.callback_query.message.message_id
        context.bot.delete_message(chat_id=chat_id, message_id=message_id)
    elif data.startswith("iscriviti"):
        printYears(update, context, first_time=False)
    else:
        checkIscriviti(update, context, data)
        checkDisiscriviti(update, context, data)

def checkIscriviti(update : Update, context : CallbackContext, data):
    if data.startswith('year'):
        if data[len(data) - 1] is "|":
            data = data[:-1]
        year = data.split('=')[1]
        printDepartment(update, context, year, data)
    elif data.startswith('dep'):
        department = (data.split('|')[0]).split('=')[1]
        year = (data.split('|')[1]).split('=')[1]
        printCdS(update, context, year, department, data)
    elif data.startswith('cds'):
        cds = (data.split('|')[0])
        max_anno = int(((data.split('|')[0]).split('=')[1]).split('_')[1])
        department = (data.split('|')[1])
        year = (data.split('|')[2])
        data = cds + '|' + department + '|' + year
        printCourseYears(update, context, max_anno, data)
    elif data.startswith('cy'):
        printSemester(update, context, data)
    elif data.startswith('sem'):
        semester = (data.split('|')[0]).split('=')[1]
        courseyear = (data.split('|')[1]).split('=')[1]
        cds = (data.split('|')[2]).split('=')[1]
        department = (data.split('|')[3]).split('=')[1]
        year = (data.split('|')[4]).split('=')[1]
        printSubject(update, context, year, department, cds[:-2], courseyear, semester, data)
    elif data.startswith('sj'):
        subject = (data.split('|')[0]).split('=')[1]
        printChoiceSubscription(update, context, subject, data)
    elif data.startswith('confSub'):
        chat_id = update.callback_query.message.chat_id
        codice_corso = (data.split('|')[1]).split('=')[1]
        confirm_subscription(chat_id, codice_corso, update, context, data)
    elif data == "reload_printYears":
        printYears(update, context, first_time=False)

def checkDisiscriviti(update: Update, context : CallbackContext, data):
    if data.startswith("confDis"):
        chat_id = update.callback_query.message.chat_id
        codice_corso = (data.split('|')[1]).split('=')[1]
        confirm_unsubscription(chat_id, codice_corso, update, context, codice_corso)
    elif data.startswith("dis"):
        if data[len(data) - 1] is "|":
            data = data[:-1]
        codice_corso = (data.split('|')[0]).split('=')[1]
        printChoiceUnSubscription(update, context, codice_corso, data)
    elif data == "reload_dis":
        printUnsubscribe(update, context, first_time=False)