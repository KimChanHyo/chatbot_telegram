
from Src import src
import time
import json
import copy

import logging

logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level = logging.INFO)

log = logging.getLogger('TimeManager.py')

class TimeManager() :
	def __init__(self) :
		self.mainTime = MyTime(self.__myMktime(time.localtime()))

	def update(self) :
		ltime = time.localtime()
		# local time = local time + 5 hour 30 min ( == 19800 sec)
		# because 18h 30m : dinner time over
		# (today's dinner time over -> have to update time to next day)
		ltime = time.localtime(int(time.mktime(ltime)) + 19800)

		if list(self.mainTime.st)[:3] != list(ltime)[:3] :
			self.mainTime = MyTime(self.__myMktime(ltime))
			return True
		return False

	# calculation day's mktime when time is 00 h 00 m 00 s
	def __myMktime(self, structTime) :
		if type(structTime) != time.struct_time :
			log.info('TimeManager.py - __myMktime function error')
			structTime = time.localtime()
		st = structTime
		st = list(st)
		st[3:6] = [0, 0, 0] # hour, min, second == 0, 0, 0
		st = time.struct_time(st)
		return int(time.mktime(st))
	
	def remainTimesToMealTime(self, structTime) :
		mealTime = [[7, 30, 0], [11, 0, 0], [17, 0, 0], 
					[8, 0, 0], [11, 30, 0], [17, 0, 0]]

		lt = structTime
		# year, mon, day, hour, min, sec, wday
		lst = list(lt)
		isWeekend = self.isWknd(lt)
		
		ret = []
		for i in range(3) :
			# dest == destination time
			if lst[3:6] < mealTime[i + isWeekend * 3] :
				dest = copy.deepcopy(lst)
				dest[3:6] = mealTime[i + isWeekend * 3]
				dest = time.struct_time(dest)
				ret.append(int(time.mktime(dest) - time.mktime(lt)))
			else :
				dest = list(time.localtime(time.mktime(lt) + 86400))
				dest[3:6] = mealTime[i + self.isWknd(time.struct_time(dest)) * 3]
				dest = time.struct_time(dest)
				ret.append(int(time.mktime(dest) - time.mktime(lt)))
		return ret
	
	def isWknd(self, structTime) :
		return (list(structTime)[6] in [5, 6])
		


class MyTime() :
	def __init__(self, val = None) :
		# val == time.struct_time or time.mktime(st)
		if type(val) == time.struct_time :
			self.st = val
			self.sec = int(time.mktime(val))
		elif type(val) == int :
			self.sec = val
			self.st = time.localtime(val)
		else :
			self.st = time.localtime(0)
			self.sec = 0 # time.mktime(st)

	def toString(self) :
		return self.__str__() + '(' + src.wday[self.st[6]] + ')'

	def __str__(self) :
		return str(self.st[1]) + '.' + str(self.st[2])

	def __repr__(self) :
		return str(self.st[0]) + '.' + self.__str__() + ' ' + str(self.sec)

	def __lt__(self, other) :
		return self.sec < other.sec

	def __le__(self, other) :
		return self.sec <= other.sec

	def __eq__(self, other) :
		return type(self) == type(other) and self.sec == other.sec

	def __ne__(self, other) :
		return type(self) != type(other) or self.sec != other.sec

	def __gt__(self, other) :
		return self.sec > other.sec

	def __ge__(self, other) :
		return self.sec >= other.sec

	def __hash__(self) :
		return self.sec

tm = TimeManager()
