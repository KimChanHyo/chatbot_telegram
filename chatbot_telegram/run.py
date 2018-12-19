
# -*- coding: euc-kr -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackQueryHandler, Filters
from Manager import manager
from Src import src

import logging

logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level = logging.INFO)

log = logging.getLogger('run.py')


def main() :
	TOKEN = 'token'
	updater = Updater(TOKEN)

	dp = updater.dispatcher

	dp.add_handler(CommandHandler('start', manager.start))
	dp.add_handler(CommandHandler('help', manager.start))
	dp.add_handler(CommandHandler('settings', manager.settings))
	for cmd in src.mealTime[:3] :
		dp.add_handler(CommandHandler(cmd, manager.meal))

	dp.add_handler(CallbackQueryHandler(manager.button))

	dp.add_error_handler(manager.error)

	log.info('run!')
	updater.start_polling()
	updater.idle()

if __name__ == '__main__' :
	main()