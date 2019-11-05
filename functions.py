# -*- coding: utf-8 -*-

# Telegram

# System libraries

# Module
from Modules.Iscrizioni import *
from Modules.Disiscrizioni import *
from Modules.Keyboard import *

# Others

def subscribed_subject_text_list(context: CallbackContext):
    msg = ""
    for subject in subscribed_subject(context.callback_query.message.chat_id):
        msg += "✅  " + subject.split("|")[0] + "\n\n"
    if msg is "":
        msg = "Non sei iscritto a nessun corso, se vuoi iscriverti lancia il comando /studium"
    context.callback_query.edit_message_text(msg)

def studium_menu(update: Update, context: CallbackContext):
    menu = ["✅ Iscriviti", "❌ Disiscriviti", "📚 Mie iscrizioni"]
    callback_menu = ["iscriviti", "disiscriviti", "mie_iscrizioni"]
    printKeyboard(context, menu, callback_menu, "", "Scegli una operazione da effettuare: ", 1, reply=True)

def buttonHandler(update: Update, context: CallbackContext):
    query = context.callback_query
    data = query.data
    print("query data = " + data)
    if data == "Esc":
        chat_id = context.callback_query.message.chat_id
        message_id = context.callback_query.message.message_id
        update.deleteMessage(chat_id=chat_id, message_id=message_id)
    elif data.startswith("iscriviti"):
        printYears(context)
    elif data.startswith("disiscriviti"):
        printUnsubscribe(context)
    elif data.startswith("mie_iscrizioni"):
        subscribed_subject_text_list(context)
    else:
        checkIscriviti(context, data)
        checkDisiscriviti(context, data)

def checkIscriviti(context, data):
    if data.startswith('year'):
        if data[len(data) - 1] is "|":
            data = data[:-1]
        year = data.split('=')[1]
        printDepartment(context, year, data)
    elif data.startswith('dep'):
        department = (data.split('|')[0]).split('=')[1]
        year = (data.split('|')[1]).split('=')[1]
        printCdS(context, year, department, data)
    elif data.startswith('cds'):
        cds = (data.split('|')[0])
        max_anno = int(((data.split('|')[0]).split('=')[1]).split('_')[1])
        department = (data.split('|')[1])
        year = (data.split('|')[2])
        data = cds + '|' + department + '|' + year
        printCourseYears(context, max_anno, data)
    elif data.startswith('cy'):
        printSemester(context, data)
    elif data.startswith('sem'):
        semester = (data.split('|')[0]).split('=')[1]
        courseyear = (data.split('|')[1]).split('=')[1]
        cds = (data.split('|')[2]).split('=')[1]
        department = (data.split('|')[3]).split('=')[1]
        year = (data.split('|')[4]).split('=')[1]
        printSubject(context, year, department, cds[:-2], courseyear, semester, data)
    elif data.startswith('sj'):
        subject = (data.split('|')[0]).split('=')[1]
        printChoiceSubscription(context, subject, data)
    elif data.startswith('confSub'):
        chat_id = context.callback_query.message.chat_id
        codice_corso = (data.split('|')[1]).split('=')[1]
        confirm_subscription(chat_id, codice_corso, context, data)
    elif data == "reload_printYears":
        printYears(context)

def checkDisiscriviti(context, data):
    if data.startswith("confDis"):
        chat_id = context.callback_query.message.chat_id
        codice_corso = (data.split('|')[1]).split('=')[1]
        confirm_unsubscription(chat_id, codice_corso, context, codice_corso)
    elif data.startswith("dis"):
        if data[len(data) - 1] is "|":
            data = data[:-1]
        codice_corso = (data.split('|')[0]).split('=')[1]
        printChoiceUnSubscription(context, codice_corso, data)
    elif data == "reload_dis":
        printUnsubscribe(context)