from globvars import *
import pygame
from pygame.locals import * 
import logic
from fruit import *
from globvars import *
import copy


def display_level_splash(game):
	level_splash=splashFont.render('Level '+str(game.get_level()),True,GREEN)
	return level_splash

def display_score(game):
	scoreText=displayFont.render('Total: '+str(game.get_score()),True,GREEN)
	return scoreText

def display_level_score(game):
	scoreWords='Score: '+str(game.get_level_score())+"/"+str(game.get_level_target())
	scoreText=displayFont.render(scoreWords,True,BLUE)
	return scoreText

def display_level(game):
	levelText=displayFont.render('Level: '+str(game.get_level()),True,RED)
	return levelText

def loadFruits(board,fruit_sprite_group):
	cell_number=1
	
	
	if len(board)>0:del board[:] #clear the board if there are any fruit objects already there (ie this is level 2+)
	
####### CREATE FRUIT OBJECTS AND LOAD THEM INTO THE LIST BOX
	
	for row in range(8):#run once for each of the 8 rows
		thisrow=[] #each row is a separate list
		y=row*CELLWIDTHHEIGHT+BOARDTOP+NUDGE #set the vertical position for the whole of the row
				
		for column in range(8):#run once for each of the 8 columns in each row
			exclude_fruits=[] #list of fruits that musn't be picked because they'd make an immediate match
			
			if column>1: #check that the two fruits to the left do not match each other (not a prob for the first 2 columns)
				if thisrow[column-2]._name==thisrow[column-1]._name: #if the two to the left are the same as this one
					exclude_fruits.append(thisrow[column-1]._name)

			if row>1: #now check whether the previous two rows hold the same fruit in this column
				if board[row-2][column]._name==board[row-1][column]._name:
					exclude_fruits.append(board[row-1][column]._name)
			
			fruit_name=logic.get_fruit(exclude_fruits) #now get a fruit from the valid choices
			
			x=column*CELLWIDTHHEIGHT+BOARDLEFT+NUDGE #set the left position of each fruit
			
			this_fruit=Fruit(fruit_name,x,y,row,column,speed,BOARDWIDTH,BOARDHEIGHT) #create a fruit object
			
			thisrow.append(this_fruit) # add a reference to the fruit object to the list for this row
		board.append(thisrow) #add the whole row to the board, as a separate sublist

def show_level_up(DISPLAYSURFACE):
	splash_surface=pygame.image.load("Graphics/levelup.jpg")
	splash_rect=splash_surface.get_rect()
	splash_rect.left=(WINDOWWIDTH-splash_rect.width)/2
	splash_rect.top=(WINDOWHEIGHT-splash_rect.height)/2
	DISPLAYSURFACE.blit(splash_surface,splash_rect)
	pygame.display.update()	


def animateFruits(board,DISPLAYSURFACE,fruit_sprite_group, BOARD_AREA,board_graphic,initial_build,game):
	
	#global speed
	##### SHOW THE ANIMATION OF THE FRUITS FALLING IN STAGGERED FASHION
	clock=pygame.time.Clock() #create a game clock for limiting the frames per second
	if initial_build==True:
		ZOOM.play()
	#else:
		#CORRECT.play()
	
	falling_fruits=[] #create a copy of the board nested list
	for fruit_row in range(8):
		falling_fruits.append(list(board[fruit_row]))

	current_row=0

	for fruit_row in reversed(falling_fruits): #the "reversed" keyword starts at the end of the list and works up
		
		fruit_sprite_group.add(fruit_row) #add all the fruit objects from this row to the sprite group ready to be displayed
		n=0
		for fruit in reversed(fruit_row): ##stagger initial positions
			fruit._speed=speed
			fruit._current_y+=n #add n to the starting position of the fruit
			n-=speed #makes n smaller (negative numbers) so the starting position goes up the screen off the page

		while len(fruit_row)>0: #while there are any fruits still in fruit_row (ie still in motion)
			
			for fruit in fruit_row: #for each fruit in the row
				fruit.move_me() #move it
				if fruit._moving==False: # if it's reached the bottom
					
					fruit_row.remove(fruit) #remove it from fruit_row
			
			shrinking_board_area=(BOARD_AREA[0],BOARD_AREA[1],BOARD_AREA[2],BOARD_AREA[3]-(CELLWIDTHHEIGHT*(current_row-1)))             #as each row is drawn, the "update" region gets smaller as the new fruits don't have as far to fall. This is an optimisation for the r-pi

			DISPLAYSURFACE.blit(board_graphic,shrinking_board_area) #only blit the bit of the board over which the fruits are falling
			
			fruit_sprite_group.draw(DISPLAYSURFACE) # draw the sprites in their new positions to the surface
			pygame.display.update(shrinking_board_area) # update only the animated part of the display
			clock.tick(60)# Limit to 60 fps
		current_row+=1
	end_of_level=game.level_check()
	
	
	return end_of_level
