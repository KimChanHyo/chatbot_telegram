
from TimeManager import tm, MyTime
import os
import json
import logging

logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level = logging.INFO)

log = logging.getLogger('DataManager.py')

class DataManager :
	def __init__(self) :
		self.__user = os.getcwd() + '\\static\\user\\'	
		self.__menu = os.getcwd() + '\\static\\menu\\'

	def addUser(self, user_id) :
		# default user settings
		# {	'alarm' : [False, False, False, False],
		#	'myTime' : tm.mainTime }
		self.setUserAlarm(user_id, [False] * 4)
		self.setUserTime(user_id, tm.mainTime)

	def getUserList(self, mealTimeIdx, structTime) :
		ret = []
		lst = os.listdir(self.__user)
		for user in lst :
			user_id = int(user[:-5]) # len('.json') == 5
			userAlarm = self.getUserAlarm(user_id)
			if userAlarm[mealTimeIdx] :
				if tm.isWknd(structTime) and not userAlarm[3] :
					continue
				ret.append(user_id)
		return ret

	def removeUser(self, user_id) :
		userPath = self.__userPath(user_id)
		if os.path.exists(userPath) :
			os.remove(userPath)

	def getUserAlarm(self, user_id) :
		userPath = self.__userPath(user_id)
		if not os.path.exists(userPath) :
			self.addUser(user_id)
		with open(userPath, 'r') as f :
			return json.loads(f.read())['alarm']

	def getUserTime(self, user_id) :
		userPath = self.__userPath(user_id)
		if not os.path.exists(userPath) :
			self.addUser(user_id)
		with open(userPath, 'r') as f :
			return MyTime(json.loads(f.read())['myTime'])

	def setUserAlarm(self, user_id, lst) :
		userPath = self.__userPath(user_id)
		
		settings = dict()
		if os.path.exists(userPath) :
			with open(userPath, 'r') as f :
				settings = json.loads(f.read())
		
		settings['alarm'] = lst
		with open(userPath, 'w') as f :
			f.write(json.dumps(settings))

	def setUserTime(self, user_id, myTime) :
		userPath = self.__userPath(user_id)
		
		settings = dict()
		if os.path.exists(userPath) :
			with open(userPath, 'r') as f :
				settings = json.loads(f.read())
		
		settings['myTime'] = str(myTime.sec)
		with open(userPath, 'w') as f :
			f.write(json.dumps(settings))

	def __userPath(self, user_id) :
		return self.__user + str(user_id) + '.json'

	def __menuPath(self, timeStruct) :
		return self.__menu + str(timeStruct.st[0]) + '.' + timeStruct.toString() + '.json'

	def getMenu(self, timeStruct) :
		menuPath = self.__menuPath(timeStruct)
		if not os.path.exists(menuPath) :
			return False
		with open(menuPath, 'r') as f :
			return json.loads(f.read())

	def saveMenu(self, meal, myTime = None) :
		menuPath = self.__menuPath(tm.mainTime if myTime == None else myTime)
		with open(menuPath, 'w') as f :
			f.write(json.dumps(meal))

dm = DataManager()