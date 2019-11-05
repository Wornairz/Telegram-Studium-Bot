# -*- coding: utf-8 -*-

# Telegram
from telegram.ext import CallbackContext

# System libraries
from datetime import datetime

# Module
from Modules.Keyboard import *
import settings

# Others
import pytz

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
        options.insert(0, str(time.year - (1-val) - x) + "/" + str((time.year + val) - x))
        values.insert(0, "year=" + str((time.year + val) - x))
    printKeyboard(context, options, values, "", "Seleziona l\'anno accademico:", 3)

def printDepartment(context, year, data):
    names = []
    values = []
    for dipartimento in settings.dipartimenti:
        if str(dipartimento["anno_accademico"]) == str(year):
            names.append("🏢 " + str(dipartimento["nome"]))
            values.append("dep=" + dipartimento["id"])
    printKeyboard(context, names, values, data, "Scegli il dipartimento:", 3)

def printCdS(context, year, department, data):
    names = []
    values = []
    for corso in settings.cds:
        if str(corso["anno_accademico"]) == str(year) and str(corso["id_dipartimento"]) == str(department):
            max_anno = getMaxAnno(corso["nome"])
            names.append("🎓 " + str(corso["nome"]))
            values.append("cds=" + str(corso["id"]) + "_" + str(max_anno))
    printKeyboard(context, names, values, data, "Scegli il corso di studio:", 2)

def printCourseYears(context, max_anno : int, data : str):
    names = []
    values = []
    for i in range(max_anno):
        names.append(str(i+1) +  "° anno")
        values.append("cy=" + str(i+1))
    printKeyboard(context, names, values, data, "Scegli l\'anno della materia:", max_anno)

def printSemester(context, data):
    names = []
    values = []
    for i in range(2):
        names.append(str(i+1) + "° semestre")
        values.append("sem=" + str(i+1))
    printKeyboard(context, names, values, data, "Scegli il semestre:", 2)

def printSubject(context, year, department, cds, courseyear, semester, data):
    names = []
    values = []
    for materia in settings.materie:
        if str(materia["anno_accademico"]) == str(year) and str(materia["id_cds"]) == str(cds):
            if(str(materia["anno"]) == str(courseyear)):
                #if(str(materia["semestre"]) == str(semester)):
                    names.append("📚 " + str(materia["nome"]))
                    values.append("sj=" + str(materia["codice_corso"]))
    printKeyboard(context, names, values, data, "Scegli la materia:", 1)

def printChoiceSubscription(context, subject, oldData):
    keyboard = [[InlineKeyboardButton("✅ Sì", callback_data = "confSub" + "|" + oldData),
                 InlineKeyboardButton("🔙 Indietro", callback_data = (oldData.split("|", 1)[1]))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    name = ""
    for materia in settings.materie:
        if str(materia["codice_corso"]) == str(subject):
            name = materia["nome"]
    context.callback_query.edit_message_text("Vuoi iscriverti a " + name + "?", reply_markup=reply_markup)

def confirm_subscription(chat_id, codice_corso, context, data):
    settings.query("INSERT INTO `Iscrizioni` (`chat_id`,`codice_corso`) VALUES (" + str(chat_id) + "," + str(codice_corso) + ");")
    printConfirmedSubscription(context, data)

def printConfirmedSubscription(context, oldData):
    keyboard = [[InlineKeyboardButton("Altre iscrizioni", callback_data = oldData.split('|', 2)[2]),
                 InlineKeyboardButton("🔚 Esci", callback_data= 'Esc')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.callback_query.edit_message_text("Iscrizione avvenuta con successo!", reply_markup=reply_markup)

def getMaxAnno(nome : str):
    if nome.find("LM", 0, len(nome)) is not -1:
        return 2
    else:
        return 3