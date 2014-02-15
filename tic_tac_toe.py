#Name : Wen Chen
#Username : wc23

########################
# In the program:
#         1. start with X , but user can choose to be X or O
#         2. since tic-tac-toe has very limited number of turns, 
#            I list all five possible situations for AI, 
#            and give corresponding strategies.
#########################
import time

def print_board():
	for i in range(0,3):
		for j in range(0,3):
			print map[2-i][j],
			if j != 2:
				print "|",
		print ""


def check_done():
# i do some revise in this part ,in order to meet the man-machine game
	flag=0
	for i in range(0,3):
		if map[i][0] == map[i][1] == map[i][2] != " " \
		or map[0][i] == map[1][i] == map[2][i] != " ":
			flag=1

	if map[0][0] == map[1][1] == map[2][2] != " " \
	or map[0][2] == map[1][1] == map[2][0] != " ":
		flag=1

	if  flag==1:
		print 
		if turn == user:
			print "U won!!!"
		else:
			print "U lose. But don't get discouraged!!"
		print 
		print "final situation:"
		print_board()
		return True

	if " " not in map[0] and " " not in map[1] and " " not in map[2]:
		print "Draw"
		print "final situation:"
		print_board()
		return True

	return False


def user_turn():
	''' user's turn .

	same as the tutorial.'''
	moved = False
	print " "
	print "7|8|9"
	print "4|5|6"
	print "1|2|3"
	while moved != True:

		try:
			pos = input("Select position by typing in the number above: ")
			if pos <= 9 and pos >= 1:
				Y=pos/3
				X=pos%3
				if X!=0:
					X-=1
				else:
					X=2
					Y-=1

				if map[Y][X]== " ":
					map[Y][X] = turn
					moved=True

		except:
			print "you need to add a numeric value"

def ai_turn(nround):
	''' ai's turn:

		AI will carry on the game in the order of the 5 strategies bellow:
		 	1. In round 1 : 
		 		**if AI is X, it should select position 5 as the start 
		 	   	  because 5 is the best position in tic-tac-toe
		 		**if AI is O, in round 1,according to situation,it has 2 solutions:
		 				i) if position 5 is still free, then select 5
		 				ii) if position 5 has been selected by user, 
		 				    then select the position in [1,3,7,9], 
		 				    which has higher possibility to win.
		 				    In the program, I set AI to choose position 1
            2. In round 2: if user keep the 5 and 9, AI should select 7 or 3. 
            				Otherwise, after user keep 5,9 and 3, AI will lose anyway.
            				Here I choose 3.
		 	3. if AI has selected two positions in a line, 
		 	   and the left one is available, then choose the left one.
		 	4. if user has selected two positions in a line, 
		 	   and the left one is available,then choose the left one.
		 	5. if there are still free positions but actually neither will win,
		 		then select the first free position AI finds.
	'''
	#s1
	if nround == 0:
		if user == "O": 
			map[1][1]=turn
		elif map[1][1]==" ":
			map[1][1]=turn
		else:
			map[0][0]=turn
		nround+=1
		return nround

	if nround == 1:
		if map[1][1]==user and map[2][2]==user:
			map[0][2]=turn
			nround+=1
			return nround
	#s2
	#horizontal search
	for h in range(0,3):
		if map[h].count(turn)==2 and map[h].count(" ")==1:
			for k in range(0,3):
				map[h][k]=turn
			return nround

	for v in range(0,3): #vertical search
		num=0
		nblank=0
		blank=0
		for n in range(0,3):
			if map[n][v]==turn:
				num+=1
			elif map[n][v]==" ":
				nblank+=1
				blank=n

		if num==2 and nblank == 1:
			map[blank][v]=turn
			return nround

	#diagonal
	if ((map[0][0]==turn and map[1][1]==turn and map[2][2]==" ") \
		or (map[0][0]==turn and map[2][2]==turn and map[1][1]==" ") \
		or (map[2][2]==turn and map[1][1]==turn and map[0][0]==" ")):
			map[0][0]=map[1][1]=map[2][2]=turn
			return nround
	if ((map[0][2]==turn and map[1][1]==turn and map[2][0]==" ") \
		or (map[0][2]==turn and map[2][0]==turn and map[1][1]==" ") \
		or (map[2][0]==turn and map[1][1]==turn and map[0][2]==" ")):
			map[2][0]=map[1][1]=map[0][2]=turn
			return nround

	#s3

	#horizontal search
	for h in range(0,3):
		if map[h].count(user)==2 and map[h].count(" ")==1:
			for k in range(0,3):
				if map[h][k]==" ":
					map[h][k]=turn
			return nround

	for v in range(0,3): #vertical search
		num=0
		nblank=0
		blank=0
		for n in range(0,3):
			if map[n][v]==user:
				num+=1
			elif map[n][v]==" ":
				nblank+=1
				blank=n

		if num==2 and nblank == 1:
			map[blank][v]=turn
			return nround

	#diagonal

	if ((map[0][0]==user and map[1][1]==user and map[2][2]==" ") \
		or (map[0][0]==user and map[2][2]==user and map[1][1]==" ") \
		or (map[2][2]==user and map[1][1]==user and map[0][0]==" ")):
			for i in range(0,3):
				if map[i][i]==" ":
					map[i][i]=turn
					return nround
	if ((map[0][2]==user and map[1][1]==user and map[2][0]==" ") \
		or (map[0][2]==user and map[2][0]==user and map[1][1]==" ") \
		or (map[2][0]==user and map[1][1]==user and map[0][2]==" ")):
			for i in range(0,3):
				if map[i][2-i]==" ":
					map[i][2-i]=turn
					return nround

	#s4
	for i in range(0,3):
		for j in range(0,3):
			if map[i][j]==" ":
				map[i][j]=turn
				return nround


	print "error!i need to rethink the algo!!DAMN IT"

################functions are over here#################

turn="X"
nround = 0
map = [[" "," "," "],
		[" "," "," "],
		[" "," "," "]]
done = False


# choose to be X or O
user = raw_input("please select to be X or O:")
if user in ['x','X']:
	user = "X"

else :
	user = "O"

while done != True:
	print
	print "current situation:"
	print_board()
	print " "
	if turn == user:
		print turn, "'s turn & user's time!!!"
		user_turn()

	else:
		print turn, "'s turn & AI's time!!!"
		time.sleep(1.5) #at least it makes me more comfortable when i play the game
		nround=ai_turn(nround)

	done = check_done()

	if done ==False:
		if turn == "X":
			turn = "O"
		else:
			turn = "X"


































