import gamePlay
from copy import deepcopy


def numCorner(board,color): #num of corners that current player has
	corner=[]
	#lefttop is marked as 1
	#leftbottom is marked as 2
	#...
	#to save time
	if board[0][0]==color:
		corner.append((0,0))
	if board[0][7]==color:
		corner.append((0,7))
	if board[7][7]==color:
		corner.append((7,7))
	if board[7][0]==color:
		corner.append((7,0))
	return corner

def markSafety(board,corner,value,color,row,column,flag,tag): #count for the value of corners and their connected pieces
	#row:position of the end-piece in row
	#column:position of the end -piece in column
	#tag represent the corner
	#recursion
	#pieces on diagonal as seeds,start from corner piece.
	start_row=corner[0]
	start_column=corner[1]
	new_row=start_row
	new_column=start_column
	if tag==0:
		for i in range(start_row,row+1):
			if board[i][start_column]==color :
				if flag[i][start_column]!=1:
					value=value+4
					flag[i][start_column]=1
				else:
					new_row=i
					break
			elif board[i][start_column]!=color:
				new_row=i
				break

		for i in range(start_column,column+1):
			if (board[start_row][i]==color):
				if flag[start_row][i]!=1:
					value=value+4
					flag[start_row][i]=1
				else:
					new_column=i
					break
			elif board[start_row][i]!=color:
				new_column=i
				break


	elif tag==1:
		for i in range(-start_row,(-row)+1):
			if (board[-i][start_column]==color): 
				if flag[-i][start_column]!=1:
					value=value+4
					flag[-i][start_column]=1
				else:
					new_row=-i
					break
			elif board[-i][start_column]!=color:
				new_row=-i
				break

		for i in range(start_column,column+1):
			if (board[start_row][i]==color): 
				if flag[start_row][i]!=1:
					value=value+4
					flag[start_row][i]=1
				else:
					new_column=i
					break
			elif board[start_row][i]!=color:
				new_column=i
				break

	elif tag==2:
		for i in range(-start_row,(-row)+1):
			if (board[-i][start_column]==color): 
				if flag[-i][start_column]!=1:
					value=value+4
					flag[-i][start_column]=1
				else:
					new_row=-i
					break
			elif board[-i][start_column]!=color:
				new_row=-i
				break

		for i in range(-start_column,(-column)+1):
			if (board[start_row][-i]==color):
				if flag[start_row][-i]!=1:
					value=value+4
					flag[start_row][-i]=1
				else:
					new_column=-i
					break
			elif board[start_row][-i]!=color:
				new_column=-i
				break

	elif tag==3:
		for i in range(start_row,row+1):
			if board[i][start_column]==color :
				if flag[i][start_column]!=1 :
					value=value+4
					flag[i][start_column]=1
				else:
					new_row=i
					break

			elif board[i][start_column]!=color:
				new_row=i
				break

		for i in range(-start_column,(-column)+1):
			if board[start_row][-i]==color : 
				if flag[start_row][-i]!=1:
					value=value+4
					flag[start_row][-i]=1
				else:
					new_column=-i
					break

			elif board[start_row][-i]!=color:
				new_column=-i
				break

	if (new_row-start_row)!=0 and (new_column-start_column)!=0:
		if tag==0:
			value=markSafety(board,(start_row+1,start_column+1),value,color,new_row,new_column,flag,tag)
		elif tag==1:
			value=markSafety(board,(start_row-1,start_column+1),value,color,new_row,new_column,flag,tag)
		elif tag==2:
			value=markSafety(board,(start_row-1,start_column-1),value,color,new_row,new_column,flag,tag)
		elif tag==3:
			value=markSafety(board,(start_row+1,start_column-1),value,color,new_row,new_column,flag,tag)

	return value

def calX(value,board,color,flag): #num of X-square the current player keeps
	for i in [(1,1),(1,6),(6,6),(6,1)]:
		if flag[i[0]][i[1]]==0:
			flag[i[0]][i[1]]=1
			if board[i[0]][i[1]]==color:
				value=value-6
	return value

def calC(value,board,color,flag): #num of C-square the current player keeps
	for i in[(0,1),(1,0),(6,0),(7,1),(0,6),(1,7),(7,6),(6,7)]:
		if flag[i[0]][i[1]]==0:
			flag[i[0]][i[1]]=1
			if board[i[0]][i[1]]==color:
				value=value-4
	return value

def edgeCount(value,board,color,flag): #num of pieces on edges 
	for i in range(2,6):
		if (flag[i][0]==0) and (board[i][0]==color):#west
			flag[i][0]=1
			value=value+2
		elif (board[i][0]=="."):
			if (board[i-1][0]==color) and (board[i+1][0]==color):
				value=value-2

		if (flag[0][i]==0) and (board[0][i]==color):#north
			flag[0][i]=1
			value=value+2
		elif (board[0][i]=="."):
			if (board[0][i-1]==color) and (board[0][i+1]==color):
				value=value-2

		if (flag[7][i]==0) and (board[7][i]==color):#south
			flag[7][i]=1
			value=value+2
		elif (board[7][i]=="."):
			if (board[7][i-1]==color) and (board[7][i+1]==color):
				value=value-2

		if (flag[i][7]==0) and (board[i][7]==color):#east
			flag[i][7]=1
			value=value+2	
		elif (board[i][7]=="."):
			if (board[i-1][0]==color) and (board[i+1][0]==color):
				value=value-2

	return value

def wallCount(value,board,color,flag): #other pieces around centroid
	for i in range(1,7):
		for j in range(1,7):
			if flag[i][j]==0 and board[i][j]==color:
				flag[i][j]==1
				signal=0
				for dicx in range(-1,2):
					for dicy in range(-1,2):
						if board[i+dicx][j+dicy]==".":
							value=value+1
							signal=1
							break
					if signal==1:
						break
				if signal==0:
					value=value+3
	return value

def evaluateFunc(board,color):
	''' Assigned different weights to different pieces according to the current situation.
		In most cases(in order),if we take:
								 (1) corner: +12  (2) all pieces if connected with corner :+4
								 (3) edge (except C): +2  (4) C:-4 (5) X:-6  
								 (6) frontier: +1. (7) Interior: +3 

		And another important point is I also consider the free pieces.Always, 
		the free pieces is 0 except it is in the edges and between two player's pieces.
		In this cases, free pieces is -2.

		for example,for a c-square, if it is connected by player-corner,the value of this square is 3 but not -3.

					
		Evaluate the value of one piece as follow strategies in order
		(we will tag all pieces to "1" that we have evaluate,and never revisit):
			1. if the player occupy the corners. We start from one corner by one corner, looking for all safe pieces .
			2. check whether occupy X and C.
			3. check the edge
			4. check free pieces on edges.
			5. check left pieces
	'''
	flag=[[0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0],
			[0,0,0,0,0,0,0,0]] 
	#if the piece has been valued ,turn "1".We just need to evaluate the 0-pieces.

	value=0
	#step 1
	corners=numCorner(board,color)
	if len(corners)!=0:
		value=9*len(corners)
		for corner in corners:
			if corner==(0,0):
				value=markSafety(board,corner,value,color,7,7,flag,0)
			elif corner==(7,0):
				value=markSafety(board,corner,value,color,7,0,flag,1)
			elif corner==(7,7):
				value=markSafety(board,corner,value,color,0,0,flag,2)
			elif corner==(0,7):
				value=markSafety(board,corner,value,color,0,7,flag,3)

	#step 2:
	value=calX(value,board,color,flag)
	value=calC(value,board,color,flag)

	#step 3 and 4:
	value=edgeCount(value,board,color,flag)

	#step 5
	value=wallCount(value,board,color,flag)

	return value


def alphabeta(limit,board,alpha,beta,turn,color):#limit is the depth of tree
	moves=[]

	if limit==0:
		''' limit=0,then return the value'''
		moveVal=evaluateFunc(board,color)
		return moveVal

	for i in range(8):
		for j in range(8):
			if gamePlay.valid(board,color,(i,j)):
				moves.append((i,j))

	if len(moves)==0: 
		''' if no moves, we just move to next turn except there is no empty block'''
		num=0
		for row in board:
			for elem in row:
				if elem=='.':
					num=num+1
		if num==0:#if no empty block,return the value
			moveVal=evaluateFunc(board,color)
			return moveVal

		if turn=="MAX":
			tmp=alphabeta(limit-1,board,alpha,beta,"MIN",color)
			if tmp>=beta:
				return beta
			else:
			 return tmp

		if turn == "MIN":
			tmp=alphabeta(limit-1,board,alpha,beta,"MAX",color)
			if tmp<beta:
				beta=tmp
				if alpha>=beta:
					return alpha
			return beta

	if turn=="MAX":
		'''MAX-VALUE FUNCTION'''
		for move in moves:
			newBoard=deepcopy(board)
			gamePlay.doMove(newBoard,color,move)
			tmp=alphabeta(limit-1,newBoard,alpha,beta,"MIN",color)
			if tmp>alpha:
				alpha=tmp
				if alpha>=beta:#pruning
					return beta
		return alpha

	if turn=="MIN":
		'''MIN-VALUE FUNCTION'''
		for move in moves:
			newBoard=deepcopy(board)
			gamePlay.doMove(newBoard,color,move)
			tmp=alphabeta(limit-1,newBoard,alpha,beta,"MAX",color)
			if tmp<beta:
				beta=tmp
				if alpha>=beta: #pruning
					return alpha
		return beta

def nextMove(board,color,time):
	decrease=0 #decrease the depth of alpha beta prunning.
	if time>=63.98:#at first, whichever piece we take, it is not a big deal.so we should save time at beginning.
		decrease=2
	elif time<17 and time>=10:
		decrease=1
	elif time<10: #when time is less than 10s
		decrease=2
	elif time<=0:
		return "pass"
	moves=[]
	bonus=[]

	for i in range(8):
		for j in range(8):
			if gamePlay.valid(board,color,(i,j)):
				moves.append((i,j))
	if len(moves)==0:
		return "pass"
	best=-100
	alpha=-100
	beta=100
	if (0,0) in moves:
		bonus.append((0,0))
	if(0,7) in moves:
		bonus.append((0,7))
	if (7,0) in moves:
		bonus.append((7,0))
	if (7,7) in moves:
		bonus.append((7,7))
	if len(bonus)>0:
		for move in bonus:
			newBoard=deepcopy(board)
			gamePlay.doMove(newBoard,color,move)
			tmp=alphabeta(2-decrease,newBoard,alpha,beta,"MIN",color)
			if best<tmp:
				best=tmp
				bestMove=move
	else:
		for move in moves:
			newBoard=deepcopy(board)
			gamePlay.doMove(newBoard,color,move)
			tmp=alphabeta(5-decrease,newBoard,alpha,beta,"MIN",color)
			if best<tmp:
				best=tmp
				bestMove=move

	return bestMove




