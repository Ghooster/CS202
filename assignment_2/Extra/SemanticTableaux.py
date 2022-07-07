"""Uses the method of semantic Tableaux to find a satisfying assignment to a given cnf formula
This is present only as a proof of concept and should not be used for any real purpose
It has an average time complexity greater than that of the trivial O(2^n) algorithm by solving truth table
This is because we discard and information gain whenever we close a node
Also note that we do not create a tree structure explicitly here but rather use the recursion tree itself"""

def driverFunction():
    path=input("Enter path of cnf file\n")
    nOfVar,nOfClauses,clauseList,varAssignments=cnfToList(path)
    print(split(nOfVar,nOfClauses,clauseList,varAssignments))

def split(nOfVar,nOfClauses,clauseList,varAssignments):
    if(nOfClauses==0):
        return varAssignments
    clause=clauseList.pop(0)
    for literal in clause:
        if(literal>0):
            if(varAssignments[literal-1]==1):
                x=split(nOfVar,nOfClauses-1,list(clauseList),list(varAssignments))
                if(x is not None):
                    return x
            elif(varAssignments[literal-1]==0):
                newVarAssignments=list(varAssignments)
                newVarAssignments[literal-1]=1
                x=split(nOfVar,nOfClauses-1,list(clauseList),newVarAssignments)
                if(x is not None):
                    return x
            elif(varAssignments[literal-1]==-1):
                x=None
        elif(literal<0):
            if(varAssignments[-literal-1]==-1):
                x=split(nOfVar,nOfClauses-1,list(clauseList),list(varAssignments))
                if(x is not None):
                    return x
            elif(varAssignments[-literal-1]==0):
                newVarAssignments=list(varAssignments)
                newVarAssignments[-literal-1]=-1
                x=split(nOfVar,nOfClauses-1,list(clauseList),newVarAssignments)
                if(x is not None):
                    return x
            elif(varAssignments[-literal-1]==1):
                x=None

def cnfToList(path="Ass2\\test.cnf"):
    """Function which reads a cnf file in DIMACS format and returns a list of clauses
    Takes the path of cnf file as input
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
driverFunction()