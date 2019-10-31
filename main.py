# -*- coding: utf-8 -*-
from functions import *
from settings import *

def main():
    updater = Updater(TOKEN, request_kwargs={'read_timeout': 20, 'connect_timeout': 20})
    
    dp = updater.dispatcher
    #dp.add_handler(MessageHandler(Filters.all, logging_message),1)
    dp.add_handler(CommandHandler('iscriviti', subscribe_course))
    dp.add_handler(CommandHandler('iscrizioni', subscribed_subject))
    dp.add_handler(CommandHandler('disiscriviti', unsubscribe_course))
    #dp.add_handler(CallbackQueryHandler(callback))
    dp.add_handler(CallbackQueryHandler(buttonHandler))

    read_db_conf()
    read_remote_db()

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()