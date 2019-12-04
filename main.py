# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

from functions import *
from settings import *

from Modules.Iscrizioni import *
from Modules.Disiscrizioni import *
from Modules.Keyboard import *

def main():
    updater = Updater(TOKEN, request_kwargs={'read_timeout': 20, 'connect_timeout': 20}, use_context=True)
    
    dp = updater.dispatcher
    #dp.add_handler(MessageHandler(Filters.all, logging_message),1)
    dp.add_handler(CommandHandler('start', startingBot))
    dp.add_handler(CommandHandler('studium', studiumMenu))
    dp.add_handler(CommandHandler('developers', getDevs))
    dp.add_handler(CommandHandler('help', getHelp))
    dp.add_handler(CommandHandler('stats', printStats))
    dp.add_handler(CommandHandler('stopspam', stopErrorMessage))

    dp.add_handler(MessageHandler(Filters.regex('✅ Iscriviti'), printYears))
    dp.add_handler(MessageHandler(Filters.regex('❌ Disiscriviti'), printUnsubscribe))
    dp.add_handler(MessageHandler(Filters.regex('📚 Mie iscrizioni'), subscribed_subject_text_list))
    dp.add_handler(MessageHandler(Filters.regex('❓ Help'), getHelp))
    #dp.add_handler(CallbackQueryHandler(callback))
    dp.add_handler(CallbackQueryHandler(buttonHandler))

    job_queue = updater.job_queue

    read_db_conf()
    job_remote_setup = job_queue.run_repeating(readRemoteDB, interval=60, first=0)
    job_avvisi = job_queue.run_repeating(forwardNotices, interval=60, first=0)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()