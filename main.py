# -*- coding: utf-8 -*-
from functions import *

with open('config/settings.yaml') as yaml_config:
	config_map = yaml.load(yaml_config)

# Token of your telegram bot that you created from @BotFather, write it on settings.yaml
TOKEN = config_map["token"]
#bot = telegram.Bot(config_map["token"])

def main():
    updater = Updater(TOKEN, request_kwargs={'read_timeout': 20, 'connect_timeout': 20})
    
    dp = updater.dispatcher
    #dp.add_handler(MessageHandler(Filters.all, logging_message),1)
    dp.add_handler(CommandHandler('iscrizione', subscribe_course))
    #dp.add_handler(CallbackQueryHandler(callback))
    dp.add_handler(CallbackQueryHandler(buttonHandler))
    read_db_conf()

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()