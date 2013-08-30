import pygame
class Cursor(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self) #we first initialise the Sprite class
		self.image=pygame.image.load("Graphics/cursor.png")
		self.rect=self.image.get_rect()#fetch the dimensions of the graphic
	
	def moveMe(self,position):
		self.rect.x=position[0]-4
		self.rect.y=position[1]-4
