import copy
from random import *
from globvars import *
def check_for_matches(board,pair_of_fruits):
	copy_board=copy.deepcopy(board) #we make a copy so that we can work on it without affecting the original
	
	#first check for row matches
	any_matches=False #use this to track if there were any matches at all
	row=0
	for fruit_row in copy_board:
		col=0
		for fruit in fruit_row:
			if col<6: #we only need to check the first 6 fruits in the row
				if fruit_row[col+1]._name==fruit_row[col+2]._name==fruit._name: 
				#are the two fruits to the right the same as this one?
					any_matches=True
					fruit._delete=True; fruit_row[col+1]._delete=True; fruit_row[col+2]._delete=True
			if row<6: #again, we only need to check the first 6 fruits in a column
				if copy_board[row+1][col]._name==copy_board[row+2][col]._name==fruit._name: 
					#are the two fruits below the same as this one?
					any_matches=True
					fruit._delete=True;copy_board[row+1][col]._delete=True;copy_board[row+2][col]._delete=True
			col+=1
		row+=1
	
	return_parameters=[any_matches]
	
	if any_matches==True:
		return_parameters.append(copy_board)
		
	return return_parameters

def check_for_neighbour(first_fruit,second_fruit):
	if second_fruit._row==first_fruit._row and second_fruit._column==first_fruit._neighbours['left']:
		return (True,'left')
	elif second_fruit._row==first_fruit._row and second_fruit._column==first_fruit._neighbours['right']:
		return (True,'right')
	elif second_fruit._row==first_fruit._neighbours['up'] and second_fruit._column==first_fruit._column:
		return (True,'up')
	elif second_fruit._row==first_fruit._neighbours['down'] and second_fruit._column==first_fruit._column:
		return (True,'down')
	else:
		return (False,None)

def handle_matches(board,pair_of_fruits):
	matches=check_for_matches(board,pair_of_fruits) # test for matches
	result=[False,False]
	
	if matches[0]==True: #if there were any matches
		delete_fruits=delete_matches(matches[1],board) #result[1] holds the copy_board if there were matches
		result[0]=True
		result[1]=delete_fruits[0]
	else:
		result[0]=False
	return result


def delete_matches(copy_board,board):
	#now assemble a list of all the fruits that are to be deleted
	delete_fruits=[]
	extra_fruits_needed=[0,0,0,0,0,0,0,0] 
	last_affected_row=[0,0,0,0,0,0,0,0] 

	row=0
	for fruit_row in copy_board:
		column=0
		for fruit in fruit_row:
			
			if fruit._delete==True:
				extra_fruits_needed[column]+=1
				last_affected_row[column]=row
				delete_fruits.append(fruit)
			column+=1
		row+=1
	
	#generate the new board
	row=0
	col=0
	for number_of_new_fruits in extra_fruits_needed:
		if number_of_new_fruits>0:
			lastrow=last_affected_row[col]
			for thisrow in range(lastrow,number_of_new_fruits-1,-1):
				board[thisrow][col]._current_y=board[thisrow-number_of_new_fruits][col]._y 
				board[thisrow][col].change_image(board[thisrow-number_of_new_fruits][col]._name,\
board[thisrow-number_of_new_fruits][col]._x,board[thisrow][col]._current_y)
				board[thisrow][col]._moving=True
				board[thisrow][col]._direction="down"

			y=-80
			for thisrow in range(0,number_of_new_fruits):
				board[thisrow][col]._current_y=y
				board[thisrow][col].change_image(get_fruit(),board[thisrow][col]._x,board[thisrow][col]._current_y)
				board[thisrow][col]._moving=True
				board[thisrow][col]._direction="down"
				y-=60
		col+=1
	
	number_of_fruits_matches=len(delete_fruits)
	return (number_of_fruits_matches,board)
	
	
def swap_fruits(pair_of_fruits,direction,board):
	
	source_fruit=pair_of_fruits["source"]
	dest_fruit=pair_of_fruits["dest"]
	tempfruit=source_fruit._name
	board[source_fruit._row-1][source_fruit._column-1].change_image(dest_fruit._name,None,None)
	board[dest_fruit._row-1][dest_fruit._column-1].change_image(tempfruit,None,None)
	return board
	

def which_fruit(board,position): #work out which fruit is under the pointer when the mouse button is pressed
	for fruit_row in board:
		for fruit in fruit_row:
			if fruit._rect.collidepoint(position):
				return fruit
				

def get_fruit(exclude_list=[]): #however many fruits there are, send back one randomly
	fruit_names=["banana","blueberry","cherry","pear","raspberry","strawberry"]

	for rottenfruit in exclude_list: #if any of the fruits are invalid
		if rottenfruit in fruit_names: fruit_names.remove(rottenfruit) #remove them from the list of choices

	fruit_name=randint(0,len(fruit_names)-1) #pick a fruit from the list of valid choices
	return fruit_names[fruit_name]
