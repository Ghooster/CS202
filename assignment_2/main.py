from copy import deepcopy       #Importing deepcopy to copy a list completely.
import sys                      #Importing sys to modify the recursion depth limit, if required.
#sys.setrecursionlimit(10000)   #Increase the recursion depth if needed
# i=0                           #Uncomment to count number of calls to solve()
import time                     #Importing time to time the code

def reduce(clauseList,literal):
    """Function to remove the occurance of the provided literal and its negation
    Takes the clauseList and literal to be removed as its arguments
    Returns the modified clause list"""
    copy=deepcopy(clauseList)
    for clause in copy:
        if(literal in clause):
            clauseList.remove(clause)   #If the literal is present in a clause as is then the clause itself is removed
        elif(literal*-1 in clause):
            clauseList.remove(clause)
            clause.remove(literal*-1)
            clauseList.append(clause)   #If the literal's negation is present then it is removed from the clause
    if [] in clauseList:
        return [[]]     #Optimising the case when a clause is empty thus unsatisfiable, returning the trivial unsat clauseList
    return clauseList
            
def solve(clauseList,varAssignments):
    # global i
    # i+=1
    # print(i)                      #Uncomment to count number of calls to solve()
    if len(clauseList)==0:
        return varAssignments       #We get a satisfying assignment when no clauses are pending
    else:
        clauseList.sort()
        clause=clauseList.pop(0)
    # We loop through each literal of the popped clause and then try assigning it the value which will make the clause true.
    # If we get a satisfying assignment for the formula then we return else we backtrack and assign it false and move to the next literal
    for literal in clause:
        if(literal>0):
            varAssignments[literal-1]=1
            newClauseList=reduce(deepcopy(clauseList),literal)
            x=solve(newClauseList,varAssignments)
            if x is not None:
                return x
            else:
                varAssignments[literal-1]=-1
                clauseList=reduce(deepcopy(clauseList),-1*literal)
        elif(literal<0):
            varAssignments[-literal-1]=-1
            newClauseList=reduce(deepcopy(clauseList),literal)
            x=solve(newClauseList,varAssignments)
            if x is not None:
                return x
            else:
                varAssignments[-literal-1]=1
                clauseList=reduce(deepcopy(clauseList),-1*literal)
    return None                     #We return none when none of theliterals produce a satisfying assignment

def cnfToList(path="test.cnf"):
    """Function which reads a cnf file in DIMACS format and returns a list of clauses
    Takes the path of cnf file as argument
    Returns a list [nOfVar,nOfClauses,clauseList,varAssignments]"""
    nOfVar=0
    nOfClauses=0
    clauseList=[]
    f=open(path)
    for i in f:
        if(i[0]=='c'):
            continue
        elif(i[0]=='p'):
            temp=i.split()
            nOfVar=int(temp[2])
            nOfClauses=int(temp[3])
            varAssignments=[0 for i in range(nOfVar)]
        else:
            clauseList.append([int(x) for x in i[:-2].split()])
    f.close()
    if(nOfClauses!=len(clauseList)):
        print("Number of clauses don't match")
        quit()
    return [nOfVar,nOfClauses,clauseList,varAssignments]

def driverFunction():
    path=input("Enter path of cnf file\n")
    t0=time.time_ns()
    nOfVar,nOfClauses,clauseList,varAssignments=cnfToList(path)
    x=solve(clauseList,varAssignments)
    t1=time.time_ns()
    if x is None:
        print("UNSAT")
    else:
        for i in range(0,nOfVar):
            if(x[i]==0):
                print(i+1,end=', ')
            else:
                print(x[i]*(i+1),end=', ')
    # print("\n",(t1-t0)/1000000000,sep='')          #Uncomment to time the code
    return

driverFunction()