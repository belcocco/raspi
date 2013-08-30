import pygame
###TOP LEVEL VARIABLES
FPS = 30 # frames per second to update the screen
WINDOWWIDTH = 1024  # width of the program's window, in pixels
WINDOWHEIGHT = 768 # height in pixels
BOARDLEFT=300 #the position of the board, from the left
BOARDTOP=50 #the position of the board, from the top
CELLWIDTHHEIGHT=82 #the width of individual cells
CELLIMAGEWIDTH=68 # the width of the image files 
BOARDWIDTH = 8 # how many columns in the board
BOARDHEIGHT = 8 # how many rows in the board
NUDGE=(CELLWIDTHHEIGHT-CELLIMAGEWIDTH)/2+4 #because the cell image is smaller than the cell, this works out how much to pad it from the left
speed=30
WHITE=[255,255,255]; RED=[255,0,0]; GREEN=[0,255,0]; BLUE=[0,100,255]; BLACK=[0,0,0]

pygame.init()
displayFont=pygame.font.Font("256BYTES.TTF",28)
splashFont=pygame.font.Font("256BYTES.TTF",48)
pygame.mixer.pre_init(frequency=44100, channels=1, buffer=1024)
pygame.mixer.init()
PLOP=pygame.mixer.Sound("plop2.wav")
ZOOM=pygame.mixer.Sound("zoom_mixdown2.wav")
CORRECT=pygame.mixer.Sound("correct2.wav")
CLICK=pygame.mixer.Sound("click.wav")
TITLE=pygame.mixer.Sound("title.wav")
