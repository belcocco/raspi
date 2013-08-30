import time, math, sys, copy
from random import randint
from pygame.locals import * 
from game import *
from fruit import *
from logic import *
from display import *
from globvars import *
from cursor import *

game=Game()

def main():
	global DISPLAYSURFACE, CLOCK #these variables will be available everywhere - keep to a minimum
	
	pygame.init()
	CLOCK=pygame.time.Clock() #create a game clock for limiting the frames per second
	DISPLAYSURFACE = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))#create a Python window the correct width and height
	pygame.display.set_caption("Fruit Pi")
	#SPLASH SCREEN
	splash=pygame.image.load("Graphics/titlescreen.jpg")
	DISPLAYSURFACE.blit(splash,(0,0))
	pygame.display.update()
	TITLE.play(-1)
	start_game=False
	game_over=False
	
	while start_game==False:
		for event in pygame.event.get():
			if event.type==pygame.KEYDOWN:
				if event.key==pygame.K_ESCAPE:
					game_over=True
					start_game=True
				elif event.key==pygame.K_RETURN or event.key==pygame.K_KP_ENTER:
					resume=False
					start_game=True

	TITLE.fadeout(1000)
	
	background=pygame.image.load("Graphics/gameBoard.png") # load a graphic to use as the background
	DISPLAYSURFACE.blit(background,(0,0)) # paint it on the surface (it won't be visible yet)
	board_graphic=pygame.image.load("Graphics/squares.png") # load the game board in 
	BOARD_AREA=board_graphic.get_rect() #get the boundaries of the board graphic
	BOARD_AREA.x=BOARDLEFT #set the board graphic's left position to the constant we defined earlier.
	BOARD_AREA.y=BOARDTOP
	DISPLAYSURFACE.blit(board_graphic,BOARD_AREA) #paint the board graphic
	pygame.display.update() # update the the display with these changes (the background and board)
	
	
	first_run=True
	
	while game_over==False:
		board=[] #a list that will contain 8 sublists (one for each row) each with 8 entries (one for each fruit)
		fruit_sprite_group=pygame.sprite.Group() #a sprite group to contain all the fruit objects
		decoration_sprite_group=pygame.sprite.Group()# [3] a sprite group to hold the cursor etc
		
		splash_running=True
		if first_run==True:
			splash_surface=pygame.image.load("Graphics/letsgo.jpg")
			first_run=False
		else:
			splash_surface=pygame.image.load("Graphics/levelup.jpg")
	
		splash_surface.convert_alpha()
		splash_rect=splash_surface.get_rect()
		alpha=254
		splash_rect.left=(WINDOWWIDTH-splash_rect.width)/2
		splash_rect.top=(WINDOWHEIGHT-splash_rect.height)/2
		DISPLAYSURFACE.blit(background,(0,0))
		DISPLAYSURFACE.blit(board_graphic,BOARD_AREA) #paint the board graphic
		DISPLAYSURFACE.blit(splash_surface,splash_rect)
		pygame.display.update()	
		pygame.time.delay(1000)
		
		
		while splash_running==True:
			splash_surface.set_alpha(alpha)
			DISPLAYSURFACE.blit(background,(0,0))
			DISPLAYSURFACE.blit(board_graphic,BOARD_AREA) #paint the board graphic
			DISPLAYSURFACE.blit(splash_surface,splash_rect)
			CLOCK.tick(50)
			
			if alpha<2:
				splash_running=False
			else:
				alpha-=4
			pygame.display.update()	
			
		re_paint=True
		level_over=False
		cursor=Cursor()
		pair_of_fruits={'source':None, 'dest':None}
		loadFruits(board,fruit_sprite_group) # create and load all the fruit objects into the board
		initial_build=True #so that the correct sound is played for the initial board build
		
		while level_over==False:
			if re_paint==True:
				redraw(background,BOARD_AREA,board_graphic,board,fruit_sprite_group,decoration_sprite_group)
				end_of_level=animateFruits(board,DISPLAYSURFACE,fruit_sprite_group,BOARD_AREA,board_graphic,initial_build,game) #draw the fruits cascading onto the screen
				
				if end_of_level==True:
					show_level_up(DISPLAYSURFACE)
					#pygame.display.update()
					#pygame.time.delay(2000)
					level_over=True
				
				initial_build=False
				result=handle_matches(board,None)
				if result[0]==True: #the board produced matches (ie after the player has removed fruit)
					game.update_score(result[1])
					CORRECT.play()
					#level_over=game.level_check()
					re_paint=True
				else:
					re_paint=False
			else:
				for event in pygame.event.get():
					if event.type==pygame.MOUSEBUTTONDOWN:
						clicked_fruit=which_fruit(board,event.pos)
						if clicked_fruit: #if the mouse has been clicked over a fruit
							CLICK.play()
							if pair_of_fruits['source']==None:
								pair_of_fruits['source']=clicked_fruit
								decoration_sprite_group.add(cursor)
								cursor.moveMe(clicked_fruit._rect)
							else:
								result=check_for_neighbour(pair_of_fruits['source'],clicked_fruit)
								is_it_a_neighbour=result[0]
								direction=result[1]
								if is_it_a_neighbour:
									pair_of_fruits['dest']=clicked_fruit
									board=swap_fruits(pair_of_fruits,direction,board)
									result=handle_matches(board,pair_of_fruits)
									if result[0]==True: #if there were matches
										pair_of_fruits['source']=None
										game.update_score(result[1])
										CORRECT.play()
										#level_over=game.level_check()
										re_paint=True
									else:
										if direction=="down":
											direction="up"
										elif direction=="up":
											direction="down"
										elif direction=="left":
											direction=="right"
										else:
											direction=="left"
										swap_fruits(pair_of_fruits,direction,board)
										
										re_paint=True
								else:
									pair_of_fruits['source']=clicked_fruit
									decoration_sprite_group.add(cursor)
									cursor.moveMe(clicked_fruit._rect)

					elif event.type==pygame.KEYDOWN:
						if event.key==pygame.K_ESCAPE:
							level_over=True
							
				if re_paint==False:redraw(background,BOARD_AREA,board_graphic,board,fruit_sprite_group,decoration_sprite_group)
				CLOCK.tick(5)
		
def redraw(background,BOARD_AREA,board_graphic,board,fruit_sprite_group,decoration_sprite_group):
	DISPLAYSURFACE.blit(background,(0,0))
	DISPLAYSURFACE.blit(board_graphic,BOARD_AREA)
	levelText=display_level(game)
	DISPLAYSURFACE.blit(levelText,(20,50))
	scoreText=display_level_score(game)
	DISPLAYSURFACE.blit(scoreText,(20,100))
	totalScoreText=display_score(game)
	DISPLAYSURFACE.blit(totalScoreText,(20,150))
	fruit_sprite_group.draw(DISPLAYSURFACE)
	decoration_sprite_group.draw(DISPLAYSURFACE)
	pygame.display.update()		


	
if __name__ == '__main__':
    main()
