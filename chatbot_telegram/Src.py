
class Src() :
	def __init__(self) :
		self.intro = '[소개]\n' + 'Koreatech 학식 메뉴를 알려주는 봇 입니다!\n' + \
			'\'\/\' 버튼을 누른 뒤, 아침, 점심, 저녁 버튼을 누르면 해당하는 메뉴를 알려주고, ' + \
			'날짜 변경 버튼을 통해 다른 날짜의 메뉴도 확인할 수 있습니다!\n' + \
			'감사합니다.'
		self.wday = ['월', '화', '수', '목', '금', '토', '일']
		self.mealTime = ['breakfast', 'lunch', 'dinner']
		self.mealType = ['한식', '일품', '특식 (전골 / 뚝배기)', '양식', '능수관', '수박여']

src = Src()
