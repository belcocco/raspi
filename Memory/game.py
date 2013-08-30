class Game():
	def __init__(self):
		self._score=0
		self._level_score=0
		self._level=1
		self._points_per_fruit=25
		self._target=500
		
		
	def level_check(self):
		
		if self._level_score>=self._target:
			self.update_level(1)
			return True
		else:
			return False
	
	def update_score(self,amount):
		self._score+=(amount*self._level)*self._points_per_fruit
		self._level_score+=(amount*self._level)*self._points_per_fruit
	
	def get_level_score(self):
		return self._level_score
	
	def get_level_target(self):
		return self._target
		
	def get_score(self):
		return self._score
		
	def update_level(self,amount):
		self._level_score=0
		self._level+=amount
		self._target=self._level*500
	
	def get_level(self):
		return self._level
'''
	def save_game(self):
		save_data={'score':self._score,'level':self._level}
		save_file=open("savedata.dat","wb")
		pickle.dump(save_data,save_file)
	
	def load_game(self):
		progress_file=open("savedata.dat","rb")
		progress_data=pickle.load(progress_file)
		self._score=progress_data['score']
		self._level=progress_data['level']
'''
