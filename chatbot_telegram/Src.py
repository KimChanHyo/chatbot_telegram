
class Src() :
	def __init__(self) :
		self.TOKEN = 'token'
		self.intro = '[소개]\n' + 'Koreatech 학식 메뉴를 알려주는 봇 입니다!\n' + \
			'- \'/\' 버튼을 누른 뒤 아침, 점심, 저녁 버튼을 누르면 해당하는 메뉴를 알려줍니다.\n' + \
			'- 다른 채팅 방에서 @KoreatechBot 을 입력하고, 식사 시간 버튼을 누르면 해당 채팅방에 메뉴를 보낼 수 있습니다.\n' + \
			'- /settings 버튼을 누르면 메뉴 미리 받기 기능을 설정할 수 있습니다.\n' + \
			'감사합니다.'
		self.wday = ['월', '화', '수', '목', '금', '토', '일']
		self.mealTime = ['breakfast', 'lunch', 'dinner']
		self.mealType = ['한식', '일품', '특식 (전골 / 뚝배기)', '양식', '능수관', '수박여']

src = Src()
