# -*- coding: utf-8 -*-

# Telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def printKeyboard(update, context, listToPrint, callbackValues, oldData, msg, nButRow, reply=False):
    keyboard = getKeyboard(listToPrint, callbackValues, oldData, nButRow)
    reply_markup = InlineKeyboardMarkup(keyboard)
    if reply:
        update.message.reply_text(msg, reply_markup=reply_markup)
    else:
        update.callback_query.edit_message_text(msg, reply_markup=reply_markup)

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
    if oldData != "":
        if oldData.find("|") == -1:
            keyboard.append([InlineKeyboardButton("🔙 Torna indietro", callback_data = "iscriviti"),
                            InlineKeyboardButton("🔚 Esci", callback_data = "Esc")])
        else:
            keyboard.append([InlineKeyboardButton("🔙 Torna indietro", callback_data= oldData.split("|", 1)[1]),
                             InlineKeyboardButton("🔚 Esci", callback_data="Esc")])
    else:
        keyboard.append([InlineKeyboardButton("🔚 Esci", callback_data="Esc")])
    return keyboard