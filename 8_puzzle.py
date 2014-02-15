import time
from pydoc import deque
from heapq import heappush, heappop
goalState = []

class Case:
	initial=0
	goal=0
	numCases=0
	def __init__(self, initial,goal,procedure):
		self.initial = initial
		self.goal=goal
		self.procedure=procedure
		Case.numCases+=1
	def setProcedure(self,procedure):
		self.procedure=procedure
	def sayInitial(self):
		return self.initial
	def sayGoal(self):
		return self.goal
	def sayProcedure(self):
		return self.procedure

# Create state from initial and goal state
def makeState(nw, n, ne, w, c, e, sw, s, se):
	statelist = [nw, n, ne, w, c, e, sw, s, se]
	for i in range(len(statelist)):# Replace blank with 0
		if statelist[i] == "blank":
			statelist[i] = 0
	return statelist


def uninformedSearch(queue,goalState,limit,numRuns):
	visited = []# List to keep track of visited nodes
	path = deque([queue])# Get first list of states in queue
	temp_path = [queue]# cloning path
	if queue == []:# If no more states available then return false
		print "No Solution Exists"
		return 0
	elif testProcedure(queue[0],goalState):# Check state is goal state and return 
		info=[numRuns,queue]
		return info
	elif limit == 0:
		print "Limit reached"
		return 0
	q = deque(queue)
	while len(q) > 0:# Get first element in queue
		n = q.popleft()
		temp_path = path.popleft()
		if n not in visited:# add node to visited nodes
			visited.append(n)
			limit -= 1
			numRuns += 1
			if queue == []:     # check for elements in queue
				print "No Solution Exists"
				return numRuns
			elif testProcedure(n,goalState):      # check if reached goal state 
				info=[numRuns,temp_path]
				return info
			elif limit == 0:
				print "Limit reached"
				return numRuns
			successors = expandProcedure(n)
			for succ in successors:
				new_path = temp_path + [succ]
				path.append(new_path)
			q.extend(successors)
	print "No Solution Exists"
	return numRuns


def testProcedure(queue,goalState):
	if (queue == goalState):
		return True
	else:
		return False

# Successor function        
def expandProcedure(state):
	successors = []
	blankPos = 0
	adjacent = []
	# Get position of blank tile
	for i in range(len(state)):
		if state[i] == 0:
			blankPos = i

	# Check whether left edge tiles
	if (blankPos % 3 != 2):
		nextPos = blankPos + 1
		adjacent.append(nextPos)


	# Check whether right edge tiles
	if (blankPos % 3 != 0):
		prev = blankPos - 1
		adjacent.append(prev)

	# Check up tile
	if (blankPos > 2):
		up = blankPos - 3
		adjacent.append(up)

	# Check down tile
	if (blankPos < 6):
		down = blankPos + 3
		adjacent.append(down)

	succ = state
	for pos in adjacent:
		succ = list(state)
	# Swap tiles and make new state. Add to successor
		if pos >= 0 and pos <= 8:
			temp = succ[blankPos]
			succ[blankPos] = succ[pos]
			succ[pos] = temp
			successors.append(succ)
	return successors


def retrivePrior(casebase,prob):
	'''retrieve prior plans.

		check whether there is similar plan(similar rate==distance<=5).
		return the similar case list
		'''


	similar_case=[]
	#each instance in similar_case has two elements: similar rate,case
	#Tell similarity by sum of initial states & goal states Manhattan Distance.The smaller score is, the better.
	print "retrieving prior cases..."
	print "there is",len(casebase),"cases in total."
	if len(casebase) <= 0:
		return similar_case

	probInitial=prob.sayInitial()
	probGoal=prob.sayGoal()
	#initial position info of them
	initPos=[0,1,2,3,4,5,6,7,8]#current problem
	goalPos=[0,1,2,3,4,5,6,7,8]
	case_initialPos=[0,1,2,3,4,5,6,7,8]#for retrieved cases
	case_goalPos=[0,1,2,3,4,5,6,7,8]
	for i in range(0,9):
		initPos[probInitial[i]]=i
		goalPos[probGoal[i]]=i


	serialNum=1
	similarcaseNum=0
	print "we use the prior case with similarity rate <=5"
	for case in casebase:
		tmpInitial=case.sayInitial()
		tmpGoal=case.sayGoal()
		print "For Case",serialNum
		serialNum+=1

		print "Initial State:"
		print (" " if tmpInitial[0] == 0 else tmpInitial[0]) , " " , (" " if tmpInitial[1] == 0 else tmpInitial[1]) , " " , (" " if tmpInitial[2] == 0 else tmpInitial[2])
		print (" " if tmpInitial[3] == 0 else tmpInitial[3]) , " " , (" " if tmpInitial[4] == 0 else tmpInitial[4]) , " " , (" " if tmpInitial[5] == 0 else tmpInitial[5])
		print (" " if tmpInitial[6] == 0 else tmpInitial[6]) , " " , (" " if tmpInitial[7] == 0 else tmpInitial[7]) , " " , (" " if tmpInitial[8] == 0 else tmpInitial[8]), "\n"
		print "Goal State:"
		print (" " if tmpGoal[0] == 0 else tmpGoal[0]) , " " , (" " if tmpGoal[1] == 0 else tmpGoal[1]) , " " , (" " if tmpGoal[2] == 0 else tmpGoal[2])
		print (" " if tmpGoal[3] == 0 else tmpGoal[3]) , " " , (" " if tmpGoal[4] == 0 else tmpGoal[4]) , " " , (" " if tmpGoal[5] == 0 else tmpGoal[5])
		print (" " if tmpGoal[6] == 0 else tmpGoal[6]) , " " , (" " if tmpGoal[7] == 0 else tmpGoal[7]) , " " , (" " if tmpGoal[8] == 0 else tmpGoal[8]), "\n"

		for i in range(0,9):
			case_initialPos[tmpInitial[i]]=i
			case_goalPos[tmpGoal[i]]=i

		distance=0
		for i in range(0,9):
			distance+=abs((case_initialPos[i]/3)-(initPos[i]/3))+abs((case_initialPos[i]%3)-(initPos[i]%3))+abs((case_goalPos[i]/3)-(goalPos[i]/3))+abs((case_goalPos[i]%3)-(goalPos[i]%3))


		print "the similarity rate is ",distance
		if distance <=5:
			similar_case.append([distance,case])

	if len(similar_case)!=0:
		print "we find",len(similar_case)," similar plan(s)"

	else:
		print "we don't find any similar plans"
	
	return similar_case


def outputProcedure(path):
	idx=0
	for i in path:
		print "Game State: ", idx
		idx+=1
		print (" " if i[0] == 0 else i[0]) , " " , (" " if i[1] == 0 else i[1]) , " " , (" " if i[2] == 0 else i[2]) 
		print (" " if i[3] == 0 else i[3]) , " " , (" " if i[4] == 0 else i[4]) , " " , (" " if i[5] == 0 else i[5]) 
		print (" " if i[6] == 0 else i[6]) , " " , (" " if i[7] == 0 else i[7]) , " " , (" " if i[8] == 0 else i[8]), "\n"


def testCaseBasedSearch(problems):
	casebase=[]
	round=1
	total_numRun=0
	for prob in problems:
		print "New prob ",round
		round+=1
		t1 = time.time()
		#similar_case=[]
		similar_case=retrivePrior(casebase,prob)
		if len(similar_case)==0:#if no similar plans
			#runs_n_path is a list of numruns and path
			runs_n_path=uninformedSearch ([prob.sayInitial()], prob.sayGoal(),20000, 0)
			t2 = time.time()
			if type(runs_n_path)!=int:
				total_numRun=runs_n_path[0]+len(casebase)
				prob.setProcedure(runs_n_path[1])

				print "find the path from scratch"
				print "Total number of runs=", total_numRun
				print "Total time of runs=",t2-t1
				print "length of path is ",len(prob.sayProcedure())
				print "the complete solution is :"
				outputProcedure(prob.sayProcedure())
				casebase.append(prob)
				print 
			else:
				print "no solution found"
				print "Total time of runs =",t2-t1
				print "Total number of runs =", runs_n_path+len(casebase)
				print 
		else:
			flag=0
			numcase=1
			total_numRun=len(casebase)
			while (flag==0):
				#try  plans in similar plans with the order of similarity(best to worst),until we find a solution
				#if we cannot find path to retrieved plan, we find path from scratch
				if len(similar_case)==0:
					runs_n_path=uninformedSearch ([prob.sayInitial()], prob.sayGoal(),20000, 0)
					if type(runs_n_path)!=int:
						t2 = time.time()
						prob.setProcedure(runs_n_path[1])
						print "find the path from scratch"
						print "Total number of runs=", runs_n_path[0]+total_numRun
						print "Total time of runs=",t2-t1
						print "length of path is ",len(prob.sayProcedure())
						print "the complete solution is :"
						outputProcedure(prob.sayProcedure())
						print 
						casebase.append(prob)
					else:
						print "No path found!"
						print "total time is ",t2-t1
						print "total number of runs is ",runs_n_path+total_numRun
						print 
					break;

				best_score=999999
				print " try plan",numcase," in similar cases:"
				numcase+=1
				loop=-1
				for case in similar_case:
					loop+=1
					if case[0]<best_score:
						best_score=case[0]
						best_case=case[1]
						mark=loop
				del similar_case[mark]
				runs_n_path_Init=uninformedSearch([prob.sayInitial()],best_case.sayInitial(),20000,0)
				runs_n_path_Goal=uninformedSearch([best_case.sayGoal()],prob.sayGoal(),20000,0)
				check_work=1
				#if we cannot find a from the current initial state to retrieved plan,
				#we skip the retrieved plan and get to the next retrieved plan
				if type(runs_n_path_Init)==int: 
					print "the plan cannot work"
					check_work=0
					total_numRun+=runs_n_path_Init
				else:
					total_numRun+=runs_n_path_Init[0]

				if type(runs_n_path_Goal)==int:
					print "the plan cannot work"
					check_work=0
					total_numRun+=runs_n_path_Goal
				else:
					total_numRun+=runs_n_path_Goal[0]

				if check_work==0:
					continue

				if check_work==1:
					flag=1
					print "Total number of runs = ",total_numRun
					path=[]
					for i in runs_n_path_Init[1]:
						path.append(i)
					path.pop()
					old_path=best_case.sayProcedure()
					for i in old_path:
						path.append(i)
					path.pop()
					for i in runs_n_path_Goal[1]:
						path.append(i)
					print "Total time of runs = ",time.time()-t1
					if old_path[0] != prob.sayInitial():
						print "the path from initial state of current problem to the state of retrieved solution:"
						outputProcedure(runs_n_path_Init[1])

					print "the path of board states of the retrieved solution:"
					outputProcedure(best_case.sayProcedure())
					if old_path[-1]!=prob.sayGoal():
						print "the path from final state of retrieved solution to goal state of current problem is:"
						outputProcedure(runs_n_path_Goal[1])

					prob.setProcedure(path)
					casebase.append(prob)
					print "length of total path is ",len(prob.sayProcedure())
					print "output the complete solution:"
					outputProcedure(prob.sayProcedure())
					print 




#Main
goalState1 = makeState(1,2,3,4,5,6,7,8,"blank")
goalState2 = makeState(1,2,3,4,5,6,7,"blank",8)
goalState3 = makeState(2,3,4,5,6,7,"blank",8,1)
#easy&similar
initialState1 = makeState(2, "blank", 3, 1, 5, 6, 4, 7, 8)
initialState2 = makeState(2, 3, "blank",1, 5, 6, 4, 7, 8)
initialState3 = makeState( "blank",2,3,1, 5, 6, 4,7, 8)
initialState4 = makeState( "blank",2, 3, 1, 5, 6, 4, 7, 8)

# easy & dissimilar
initialState5 = makeState(1, 2, 3, 4, 5,6, 7, "blank", 8)
initialState6 = makeState(2, "blank", 3, 1, 5, 6, 4, 7, 8)
initialState7 = makeState(1, "blank", 3, 5, 2, 6, 4, 7, 8)
initialState8 = makeState(1, 2, 3, "blank", 4, 6, 7, 5, 8)

# hard & similar
initialState9 = makeState(2, 6, 5, 4, "blank", 3, 7, 1, 8)
initialState10 = makeState(2, 6, 5, "blank", 4,3, 7, 1, 8)
initialState11 = makeState(2, 6, 5, 4, 3,"blank",  7, 1, 8)
initialState12 = makeState(2, "blank", 5, 4, 6, 3, 7, 1, 8)

# hard & dissimilar
initialState13 = makeState(2, 6, 5, 4, "blank", 3, 7, 1, 8)
initialState15 = makeState(3, 6, "blank", 5, 7, 8, 2, 1, 4)
initialState14 = makeState(1, 5, "blank", 2, 3, 8, 4, 6, 7)
initialState16 = makeState(2, 5, 3, 4, "blank", 8, 6, 1, 7)

case1=Case(initialState1,goalState1,0)
case2=Case(initialState2,goalState1,0)
case3=Case(initialState3,goalState1,0)
case4=Case(initialState4,goalState1,0)

case5=Case(initialState5,goalState1,0)
case6=Case(initialState6,goalState1,0)
case7=Case(initialState7,goalState1,0)
case8=Case(initialState8,goalState1,0)

case9=Case(initialState9,goalState1,0)
case10=Case(initialState10,goalState1,0)
case11=Case(initialState11,goalState1,0)
case12=Case(initialState12,goalState1,0)

case13=Case(initialState13,goalState1,0)
case14=Case(initialState14,goalState1,0)
case15=Case(initialState15,goalState1,0)
case16=Case(initialState16,goalState1,0)

problems1=[case1,case2,case3,case4]#easy x similar
problems2=[case5,case6,case7,case8]
problems3=[case9,case10,case11,case12]
problems4=[case13,case14,case15,case16]
print 
print "==============================="
print "Test problem list: generate solutions for easy x similar problems"
print "==============================="
print 
testCaseBasedSearch(problems1)
print
print "==============================="
print "Test problem list: generate solutions for easy x dissimilar problems"
print "==============================="
print 
testCaseBasedSearch(problems2)
print 
print "==============================="
print "Test problem list: generate solutions for hard x similar problems"
print "==============================="
print
testCaseBasedSearch(problems3)
print 
print "==============================="
print "Test problem list: generate solutions for hard x dissimilar problems"
print "==============================="
print
testCaseBasedSearch(problems4)













