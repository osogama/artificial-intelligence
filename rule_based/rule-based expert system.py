#As a sample to you, for convenience,I have simplified the system into a text file,combining several python files into one.
#it is a simple expert system,which will produce new knowlege into knowledge base according to current knowledge and rules.
#test rules are in rlwm.py
#my test rules is about organism classification
#rules stands for rules ,and wm stands for the initial knowledge base
#sample_output gives a sample output

from pydoc import deque
from copy import deepcopy
import rlwm

class State:
	def __init__(self, antec,sub):
		self.antec=antec
		self.sub=sub
	def get_antec(self):
		return self.antec
	def get_sub(self):
		return self.sub
	def update_sub(self,sub):
		self.sub=sub
	def update_antec(self,antec):
		self.antec=antec


def substitute(substitution,pattern):
	'''substitution:[['?a1',a1],['?b1','b1']...]
		pattern:['a',...,'?s',...]
	'''
	for i in range(len(pattern)):
		if pattern[i][0]=='?':
			for sub in substitution:
				if sub[0]==pattern[i]: #assume no paradoxical sub in subs
					pattern[i]=sub[1]
					break
	return pattern

def unify_var(var,pat,subs):
	flag=0
	tmp_var=deepcopy(var)
	tmp_pat=deepcopy(pat)
	for i in range(len(var)):
		if tmp_var[i][0]=='?':
			for sub in subs:
				if sub[0]==tmp_var[i]:
					tmp_var[i]=sub[1]
					flag=1
					break
			if flag==1:#If var has a binding in substitution, call unify with the new value and pat
				return unify(tmp_var,tmp_pat,subs)
			else:#Else apply the substitution to pat. If var appears anywhere in the result of the substitution, return #f.
				tmp=[var[i],pat[i]]
				next=pat[i]
				t=pat[i]
				while True:#examine ?cycle
					for sub in subs:
						if sub[0]==t:
							next=sub[1]
							break

					if next==var[i]:# cycle exists
						return False
					if next==t:# right binding
						break
					else:#next step
						t=next

				subs.append(tmp)
				return subs


def unify(pat1,pat2,subs):
	''' slightly modify from the algo in lecture to meet the expect system:
		delete some functions that cannot happens in my codes for pat1 is antec and pat2 is current wm
		pat1: antec ['k','?k',...]
		pat 2:wm_left[0]
		subs:[['?x',a],['?s',d],...]


		#f in unify:
		1.cycle((?x ?y) (?y ?x))
		2.different atom['a','?x'],['x','?x']
		3.different substitution for a same var

		return [[?a,a],[?b,b],...] updated substituion
		'''
	new_subs=deepcopy(subs)
	#print "in unify"
	#print pat1
	#print pat2

	if len(pat1)!=len(pat2):
		return False

	if pat1==pat2:#?equal
		return subs

	for i in range(len(pat1)):
		if pat1[i]==pat2[i]:
			continue
		elif pat1[i][0]=='?':
			tmp=unify_var(pat1,pat2,new_subs)
			if tmp==False:
				return False
			else:
				new_subs=tmp
		elif (isinstance(pat1[i],list) and isinstance(pat2[i],list))==False:
			return False
		else:#both are list
			tmp=unify(pat1[i],pat2[i],subs)

			if tmp==False:
				return False
			else:
				new_subs=tmp
	return new_subs




def match_antecedent(anteceds,wm,subs):
	'''return all possible states from first antecedent

	'''
	antec=anteceds[0]
	remain_antec=[]
	for i in range(len(anteceds)):
		if i!=0:
			remain_antec.append(anteceds[i])
	def ma_helper(states,wm_left):
		if len(wm_left)==0:
			return states
		else:
			tmp=unify(antec,wm_left[0],subs)

			if tmp!=False:
				new_state=State(remain_antec,tmp)
				states.append(new_state)
			new_wm=[]
			for i in range(len(wm_left)):
				if i!=0:
					new_wm.append(wm_left[i])
			ma_helper(states,new_wm)
		return states
	states=[]
	states=ma_helper(states,wm)
	return states

def execute(subs,rhs,wm):
	''' return the list of new patterns

	'''
	new_pattern=[]
	tmprhs=deepcopy(rhs)
	for rule in tmprhs:
		flag=0
		tmp=substitute(subs,rule)
		for i in wm:
			if i == tmp:
				flag=1
				break
		if flag==0:
			new_pattern.append(tmp)

	return new_pattern


def match_rule(rule_id,lhs,rhs,wm):
	'''return the list of new patterns

	'''
	print "Attempting to match rule",rule_id
	def mr_helper(queue,new_wm):
		if len(queue)==0:
			if len(new_wm)==0:# to trace the running info
				print "Failing"
			else:
				print "Match succeeds"
				print "Adding assertions to WM:"
				print new_wm
				print 
			return new_wm
		else:
			state1=queue.pop()
			if len(state1.get_antec())==0:#state1 is the goal state
				tmp=execute(state1.get_sub(),rhs,wm)
				new_wm.extend(tmp)
				mr_helper(queue,new_wm)
			else:
				tmp=match_antecedent(state1.get_antec(),wm,state1.get_sub())
				if len(tmp)==0:
					mr_helper(queue,new_wm)
				else:
					queue.extend(tmp)
					mr_helper(queue,new_wm)
		return new_wm

	tmplhs=deepcopy(lhs)
	current_queue=match_antecedent(tmplhs,wm,[])
	#print current_queue[0].get_sub()
	return mr_helper(current_queue,[])


def match_rules(rules,wm):
	new_pat=[]#[[pat1],[pat2],....]
	tmpRules=deepcopy(rules) #make deepcopy of rules and wm, to guarantee not changing them in procedure
	antecedents=[]
	consequents=[]
	for rule in rules:# get the LHS and RHS
		antecedents.append(rule[1])
		consequents.append(rule[2])
	tmpwm=deepcopy(wm)
	for i in range(len(rules)):#call math_rule to each of rules,and extend(append) new patterns to new_pat
		new_pat.extend(match_rule(i+1,antecedents[i],consequents[i],tmpwm))
	return new_pat

def run_ps(rules,wm):
	flag=True
	cycle=1
	while flag:
		print "CYCLE",cycle
		print 
		print "Current WM:"
		for i in range(len(wm)):
			print wm[i]
		print 
		cycle=cycle+1
		new_patterns=match_rules(rules,wm)# [[pat1],[pat2]]
		if len(new_patterns)!=0:
			wm.extend(new_patterns)
		else:
			print "NO CHANGES ON LAST CYCLE,HALTING"
			print
			flag=False
	return wm




#Main

updated_wm=run_ps(rlwm.rules,rlwm.wm)
wm=updated_wm
print "Final Working Memory:"
print wm
			