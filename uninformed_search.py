import time

def makeNode(state, parent, depth, pathCost):
    return [state, parent, depth, pathCost]

def makeState(nw, n, ne, w, c, e, sw, s, se):
    #Generates and returns a (board) state based on the given arguments 
    board=[nw,n,ne,
        w,c,e,
        sw,s,se]
    return board

def print_board(board):
    for i in range(0,9):
        if board[i]=="blank":
            print " " ,
        else:
            print board[i] ,
        if i%3 != 2:
            print "|",
        else:
            print ""
    print""

def getProc(node,solution):
    if node[2]!=0:
        solution.append(node[0])
        getProc(node[1],solution)
    else:
        solution.append(node[0])
        while len(solution) != 0:
            print_board(solution.pop())
        return 

def outPutprocedure(node):
    solution=[]
    solution=getProc(node,solution)

def testProcedure(node,goal):
    if node[0] == goal:
        flag=1
        outPutprocedure(node)
    else:
        flag=0
    return flag




def generalSearchuni(queue,explored,limit,pathCost,goal):
    while limit >= 0:
        if queue == []:
            return False
        nodeCurrent=queue.pop() #current node
        explored.append(nodeCurrent[0]) #push the current node into explored list
        temp=[]
        for i in range(0,9):
            temp.append(nodeCurrent[0][i])
        BlankPosition=temp.index("blank")
        xx=BlankPosition%3
        yy=BlankPosition/3
        if xx != 0:
            ''' blank move to left
                in the other words, the action is right'''
            pathCost=pathCost+1
            a=temp[BlankPosition-1]
            temp[BlankPosition-1]="blank"
            temp[BlankPosition]=a
            child=makeNode(temp,nodeCurrent,nodeCurrent[2]+1,pathCost)
            if (child not in queue) or (child[0] not in explored):
                #  print_board(child[0])
                limit=limit-1
                flag=testProcedure(child,goal)
                if flag==1:
                    print "#run is",child[3]
                    return flag
                queue.insert(0,child)

        if xx != 2:
            ''' blank move to right
                the action is left'''
            temp=[]
            for i in range(0,9):
                temp.append(nodeCurrent[0][i])
            pathCost=pathCost+1
            a=temp[BlankPosition+1]
            temp[BlankPosition+1]="blank"
            temp[BlankPosition]=a
            child=makeNode(temp,nodeCurrent,nodeCurrent[2]+1,pathCost)
            if (child not in queue) or (child[0] not in explored):
             #   print_board(child[0])
                flag=testProcedure(child,goal)
                limit=limit-1
                if flag==1:
                    print "#run is",child[3]
                    return flag
                queue.insert(0,child)
        if yy != 0:
            '''blank move up
               the action is down'''
            temp=[]
            for i in range(0,9):
                temp.append(nodeCurrent[0][i])
            pathCost=pathCost+1
            a=temp[BlankPosition-3]
            temp[BlankPosition-3]="blank"
            temp[BlankPosition]=a
            child=makeNode(temp,nodeCurrent,nodeCurrent[2]+1,pathCost)
            if (child not in queue) or (child[0] not in explored):
            #    print_board(child[0])
                flag=testProcedure(child,goal)
                limit=limit-1
                if flag==1:
                    print "#run is",child[3]
                    return flag
                queue.insert(0,child)
        if yy != 2:
            ''' blank move down
                the action is up'''
            temp=[]
            for i in range(0,9):
                temp.append(nodeCurrent[0][i])
            pathCost=pathCost+1
            a=temp[BlankPosition+3]
            temp[BlankPosition+3]="blank"
            temp[BlankPosition]=a
            child=makeNode(temp,nodeCurrent,nodeCurrent[2]+1,pathCost)
            if (child not in queue) or (child[0] not in explored):
                flag=testProcedure(child,goal)
                limit=limit-1
                if flag==1:
                    print "#run is",child[3]
                    return flag
                queue.insert(0,child)

    if limit > 0:
        print "wrong"
    elif limit <= 0:
        return 2

def testUninformedSearch(init, goal, limit):
    ''' Breadth-first search'''
    node=makeNode(init,0,0,0)
    testProcedure(node,goal)
    queue=[node] #list of unexplored nodes
    explored=[] #list of explored states
    pathCost=1
    print "new exp"
    startTime=time.clock()
    flag=generalSearchuni(queue,explored,limit,pathCost,goal)
    finalTime=time.clock()
    print " during time is",finalTime-startTime
    if flag==2:
        print "in the Limit time, the algo can't find the procedure"
        print ""
    if flag==False:
        print "there is no procedure to reach the goal"
        print ""


goalState=makeState(1,2,3,4,5,6,7,8,"blank")
# First group of test cases - should have solutions with depth <= 5
initialState1 = makeState(2, "blank", 3, 1, 5, 6, 4, 7, 8)
##
# Second group of test cases - should have solutions with depth <= 10
initialState9 = makeState(1, 3, "blank", 4, 2, 6, 7, 5, 8)
##
# Third group of test cases - should have solutions with depth <= 20
initialState14 = makeState(1, 2, 3, 5, "blank", 6, 4, 7, 8)
##
# Fourth group of test cases - should have solutions with depth <= 50
initialState19 = makeState(2, 5, 3, 4, "blank", 8, 6, 1, 7)
limit=2000
initialState=initialState1
testUninformedSearch(initialState,goalState,limit)
initialState=initialState9
testUninformedSearch(initialState,goalState,limit)
initialState=initialState14
testUninformedSearch(initialState,goalState,limit)
initialState=initialState19
testUninformedSearch(initialState,goalState,limit)





