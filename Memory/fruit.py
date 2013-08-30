import pygame
from globvars import *

class Fruit(pygame.sprite.Sprite): #create a Fruit class and base it on pygame's Sprite
#each of the 64 fruits is an individual instance of this class, each with its own properties
	
	
	def __init__(self,image_name,x,y,row,column,speed,BOARDWIDTH,BOARDHEIGHT): #this is carried out when the fruit is created [3]
		pygame.sprite.Sprite.__init__(self) #we first initialise the Sprite class
		self.image=pygame.image.load("Graphics/"+image_name+".png")
		self.image.convert()
		#SET INSTANCE VARIABLES
		self._name=image_name #this is the fruit - eg "raspberry".
		self._x=0; self._y=0; #_x and _y are the positions the fruit will occupy on the board
		self._current_y=0 # this is the current position (eg as it's falling into place)
		self._current_x=0
		self._moving=False #if it's moving, this will be True
		self._speed=speed # this is the number of pixels to move per cycle
		self._rect=(0,0,0,0)
		self._row=0
		self._column=0
		self._left=0
		self._x=x #the final position
		self._y=y
		self._moving=True
		self._row=row+1 #
		self._column=column+1 # #row and column are one based so the top row is row 1
		self._direction="down" # when first created, the initial direction is always down
		self._delete=False #once matched, this will become True
		self._neighbours={'left':None,'up':None,'right':None,'down':None}
		#self.plop=pygame.mixer.Sound("plop2.wav")
		self.calculate_neighbours(BOARDWIDTH,BOARDHEIGHT)
		
	def change_image(self,image_name,x=None,y=None):
		self._name=image_name
		self.image=pygame.image.load("Graphics/"+image_name+".png")
		self.rect=self.image.get_rect() #get the dimensions of the fruit image
		if x!=None:
			self.rect.x=x
		else:
			self.rect.x=self._x
			
		if y!=None:
			self.rect.y=y
		else:
			self.rect.y=self._y
	
	def calculate_neighbours(self,BOARDWIDTH,BOARDHEIGHT): #used for fruit swapping
		
		if self._column>1:
			self._neighbours['left']=self._column-1 #if this fruit is in the second column or later, it must have a neighbour on its left
			self._left=self._column-1
		if self._row>1:self._neighbours['up']=self._row-1
		if self._column<BOARDWIDTH:self._neighbours['right']=self._column+1 # if the fruit is in columns 1-7, it'll have a right neighbour
		if self._row<BOARDHEIGHT:self._neighbours['down']=self._row+1 

		
	def move_me(self):
		if self._moving==True: #if the fruit hasn't reached its final position
			self.calculate_new_position(self._direction) #calculate the next point in the trajectory
	

	
		
	def calculate_new_position(self,direction): #add direction
		if direction=="down":
			if (self._current_y  + self._speed) < self._y: #if it's not nearly at the bottom of its column
				self._current_y+=self._speed # add the next increment
			else:
				self._current_y=self._y # set the y (up and down) of this object to the final resting place
				self._moving=False
				
		elif direction=="up":
			if(self._current_y - self._speed) > self._y:
				self._current_y-=self._speed
			else:
				self._current_y=self._y # set the y (up and down) of this object to the final resting place
				self._moving=False
		elif direction=="right":
			if (self._current_x  + self._speed) < self._x: #if it's not nearly at the bottom of its column
				self._current_x+=self._speed # add the next increment
			else:
				self._current_x=self._x # set the y (up and down) of this object to the final resting place
				self._moving=False
		elif direction=="left":
			if(self._current_x - self._speed) > self._x:
				self._current_x-=self._speed
			else:
				self._current_x=self._x # set the x (left and right) of this object to the final resting place
				self._moving=False
		
		self.rect=self.image.get_rect() #get the dimensions of the fruit image
		if direction=="up" or direction=="down":
			self.rect.y=self._current_y # set the y (up and down) dimension of the image to the new setting
			self.rect.x=self._x #set the x (left to right) dimension to the object's setting
		else:
			self.rect.y=self._y # set the y (up and down) dimension of the image to the new setting
			self.rect.x=self._current_x #set the x (left to right) dimension to the object's setting
		self._rect=self.rect #[3] store the rect for use later
