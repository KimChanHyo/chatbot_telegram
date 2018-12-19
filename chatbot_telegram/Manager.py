
from Src import src
from Menu import menu
from TimeManager import tm, MyTime
from DataManager import dm

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot

import time
import threading
import logging

logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level = logging.INFO)

log = logging.getLogger('Manager.py')

class Manager() :
	def __init__(self) :
		TOKEN = 'token'
		self.__bot = Bot(TOKEN)
		remainTimes = tm.remainTimesToMealTime(time.localtime())
		log.info('__init__ - remainTimes : ' + str(remainTimes))
		for i in range(3) :
			self.__t = threading.Timer(remainTimes[i], self.__sendMessage, (i, ))
			self.__t.start()
		
		self.__onOffKeyboard = InlineKeyboardMarkup([[InlineKeyboardButton('On', callback_data = 'On'),
								InlineKeyboardButton('Off', callback_data = 'Off')]])
	def __del__(self) :
		self.__t.cancel()

	def meal(self, bot, update) :
		if tm.update() :
			menu.update()
		mealTime = update.message.text[1:]
		update.message.reply_text(menu.getMeal(mealTime, tm.mainTime))

	def start(self, bot, update) :
		update.message.reply_text(src.intro)

	def settings(self, bot, update) :
		user_id = update.message.from_user.id
		log.info('settings' + str(id))
		
		update.message.reply_text(	'저희 봇은 식사시간 전에(약 30분 전) 자동으로 메뉴를 보내주는 기능이 있습니다.\n' + \
									'사용하시려면 아침, 점심, 저녁, 주말에 대해 수신 여부를 설정해주십시오.\n\n')
		update.message.reply_text(self.__onOffText(dm.getUserAlarm(user_id), 0),
									reply_markup = self.__onOffKeyboard)
	def button(self, bot, update) :
		q = update.callback_query
		text = q.message.text
		user_id = q.from_user.id
		onOff = True if q.data == 'On' else False
		
		alarm = dm.getUserAlarm(user_id)
		mealTime = src.mealTime + ['weekend']
		for i in range(len(mealTime)) :
			if mealTime[i] in text :
				idx = i
				break
		alarm[idx] = onOff
		dm.setUserAlarm(user_id, alarm)
		if idx < 3 :
			bot.edit_message_text(self.__onOffText(alarm, idx + 1),
									chat_id = q.message.chat_id,
									message_id = q.message.message_id,
									reply_markup = self.__onOffKeyboard)
		else :
			replyText = '설정이 완료되었습니다!\n'
			for i in range(len(mealTime)) :
				replyText += mealTime[i] + ' : ' + ('On' if alarm[i] else 'Off') + '\n'
			bot.edit_message_text(replyText, chat_id = q.message.chat_id, message_id = q.message.message_id)

	def __onOffText(self, alarm, idx) :
		mealTime = src.mealTime + ['weekend']
		return mealTime[idx] + ' (현재 ' + \
				('On' if alarm[idx] else 'Off') + ')'

	def __sendMessage(self, mealTimeIdx) :
		if tm.update() :
			menu.update()

		myTime = tm.mainTime
		meal = menu.getMeal(src.mealTime[mealTimeIdx], myTime)

		userList = dm.getUserList(mealTimeIdx, myTime.st)
		for user_id in userList :
			self.__bot.send_message(user_id, meal)

		myTime = MyTime(myTime.sec + 30)
		remainTime = tm.remainTimesToMealTime(myTime.st)[mealTimeIdx]
		self.__t = threading.Timer(remainTime, self.__sendMessage, (mealTimeIdx, ))
		self.__t.start()
		

	def error(self, bot, update, error) :
		log.warning('Update "%s" caused error "%s"', update, error)

manager = Manager()