import numpy as np
import random
from pysat.solvers import Solver

k=int(input("Enter k\n"))
if(k==1):
    print("Sudoku pair not possible")
    quit()
#x[i][j][v] is a boolean variable which stores if the value at ith row, jth column of the first sudoku is v or not. Similarily, for 2nd sudoku we have y.
x=[[[0 for i in range(k*k)] for j in range(k*k)] for v in range(k*k)]
y=[[[0 for i in range(k*k)] for j in range(k*k)] for v in range(k*k)]
for i in range(0,(k*k)):
    for j in range(0,(k*k)):
        for v in range(0,(k*k)):
            x[i][j][v]=((i)*(k**4)) + ((j)*k*k) + v + 1         #Maps x[i][j][v] to a unique integer (((i)*(k**4)) + ((j)*k*k) + v + 1 )
            y[i][j][v]=((i)*(k**4)) + ((j)*k*k) + v + k**6 + 1  #Maps x[i][j][v] to a unique integer (((i)*(k**4)) + ((j)*k*k) + v + k**6 + 1)

cnf=[]      #Stores the list of formulae in cnf form for the pysat object
Temp=[]

#Condition to assure that a cell has a non zero value
for i in range(0,k*k):
    for j in range(0,k*k):
        for v in range(0,k*k):
            Temp.append(x[i][j][v])
        cnf.append(list(Temp))
        Temp.clear()
#Condition to check that a cell has no more than 1 value
for i in range(0,k*k):
    for j in range(0,k*k):
        for v1 in range(0,k*k):
            for v2 in range(v1+1,k*k):
                cnf.append([-1*x[i][j][v1],-1*x[i][j][v2]])
#Row constraints
for i in range(0,k*k):
    for v in range(0,k*k):
        for j in range(0,k*k):
            Temp.append(x[i][j][v])
        cnf.append(list(Temp))
        Temp.clear()
#Column constraints
for j in range(0,k*k):
    for v in range(0,k*k):
        for i in range(0,k*k):
            Temp.append(x[i][j][v])
        cnf.append(list(Temp))
        Temp.clear()
#Mini grid (k*k) constraints
for v in range(0,k*k):
    for i0 in range(0,k):
        for j0 in range(0,k):
            for i in range(i0*k,(i0+1)*k):
                for j in range(j0*k,(j0+1)*k):
                    Temp.append(x[i][j][v])
            cnf.append(list(Temp))
            Temp.clear()

#Repeating the same conditions for the second sudoku, y

#Condition to assure that a cell has a non zero value
for i in range(0,k*k):
    for j in range(0,k*k):
        for v in range(0,k*k):
            Temp.append(y[i][j][v])
        cnf.append(list(Temp))
        Temp.clear()
#Condition to check that a cell has no more than 1 value
for i in range(0,k*k):
    for j in range(0,k*k):
        for v1 in range(0,k*k):
            for v2 in range(v1+1,k*k):
                cnf.append([-1*y[i][j][v1],-1*y[i][j][v2]])
#Row constraints
for i in range(0,k*k):
    for v in range(0,k*k):
        for j in range(0,k*k):
            Temp.append(y[i][j][v])
        cnf.append(list(Temp))
        Temp.clear()
#Column constraints
for j in range(0,k*k):
    for v in range(0,k*k):
        for i in range(0,k*k):
            Temp.append(y[i][j][v])
        cnf.append(list(Temp))
        Temp.clear()
#Mini grid (k*k) constraints
for v in range(0,k*k):
    for i0 in range(0,k):
        for j0 in range(0,k):
            for i in range(i0*k,(i0+1)*k):
                for j in range(j0*k,(j0+1)*k):
                    Temp.append(y[i][j][v])
            cnf.append(list(Temp))
            Temp.clear()

#Mutual constraint
for i in range(0,k*k):
    for j in range(0,k*k):
        for v in range(0,k*k):
            cnf.append([-1*x[i][j][v],-1*y[i][j][v]])

#New code

cnfCopy=list(cnf)
s=Solver()
#Generating a (pseudo)random sudoku pair
while True:
    rand=[i for i in range(0,k)]
    random.shuffle(rand)
    v=[i for i in range(1,(k*k)+1)]
    for i0 in range(0,k):
        random.shuffle(v)
        t=0
        for i in range(i0*k,(i0+1)*k):
            for j in range(rand[i0]*k,(rand[i0]+1)*k):
                cnf.append([x[i][j][v[t]-1]])
                t=t+1
    random.shuffle(cnf)
    s.delete()
    s=Solver()
    s.append_formula(cnf)
    s.solve()
    result=s.get_model()
    if result is None:
        cnf=list(cnfCopy)
        continue
    else:
        break

s.delete()
s=Solver()
cnf=list(cnfCopy)
Temp2=[]
solution=list(result)
for i in range(0,2*(k**6)):
    if(result[i]>0):
        Temp.append(-1*(i+1))
        Temp2.append([i+1])

cnfCopy1=list(cnfCopy)
cnfCopy1.append(list(Temp))
cnf.append(list(Temp))
random.shuffle(Temp2)

t=0
#Looping through a shuffled list of values at the cells and deleting them one by one and then checking if a new solution crops up or not.
for i in range(0,2*k**4):
    x=Temp2.pop(t)
    cnf=list(cnfCopy1)
    cnf=cnf+Temp2
    s=Solver()
    s.append_formula(cnf)
    s.solve()
    result=s.get_model()
    s.delete()
    if result is None:
        continue
    else:
        Temp2.insert(t,x)
        t=t+1

s1=[[[0 for i in range(k*k)] for j in range(k*k)] for v in range(k*k)]
s2=[[[0 for i in range(k*k)] for j in range(k*k)] for v in range(k*k)]

for t in Temp2:
    if(t[0]<k**6):
        i=(t[0]-1)//(k**4)
        j=(t[0]-i*(k**4)-1)//(k*k)
        v=(t[0]-i*(k**4)-j*k*k-1)
        s1[i][j][v]=1
    else:
        i=(t[0]-1-(k**6))//(k**4)
        j=(t[0]-i*(k**4)-1-(k**6))//(k*k)
        v=(t[0]-k**6-i*(k**4)-j*k*k-1)
        s2[i][j][v]=1

        
s=''
print("Sudoku 1")
for i in range(0,k*k):
    for j in range(0,k*k):
        t=0
        for v in range(0,k*k):
            if(s1[i][j][v]>0):
                print(v+1,end=',')
                if(j!=k*k-1):
                    s=s+str(v+1)+','
                else:
                    s=s+str(v+1)
                t=1
        if(t==0):
            if(j!=k*k-1):
                s=s+'0,'
            else:
                s=s+'0'
            print(0,end=',')
    print('\b ')
    s=s+'\n'

print("Sudoku 2")
for i in range(0,k*k):
    for j in range(0,k*k):
        t=0
        for v in range(0,k*k):
            if(s2[i][j][v]>0):
                if(j!=k*k-1):
                    s=s+str(v+1)+','
                else:
                    s=s+str(v+1)
                print(v+1,end=',')
                t=1
        if(t==0):
            if(j!=k*k-1):
                s=s+'0,'
            else:
                s=s+'0'
            print(0,end=',')
    print('\b ')
    s=s+'\n'
with open("MaximalPair.csv", "w") as text_file:
    text_file.write(s)
        
print("\n\nUnique Solution:")
s=''
count=0
print("Sudodu #1:")
for i in range(0,k**6):
    if(solution[i]>0):
        if(solution[i]%(k*k)>0):
            print(solution[i]%(k*k),end='')
            s=s+str(solution[i]%(k*k))+''
        else:
            print(k*k,end='')
            s=s+str(k*k)+''
        count=count+1
        if(count%(k*k)==0):
            print('')
            s=s+'\n'
        else:
            print(',',end='')
            s=s+','
print("\nSudodu #2:")
count=0
for i in range(k**6,2*(k**6)):
    if(solution[i]>0):
        if(solution[i]%(k*k)>0):
            print(solution[i]%(k*k),end='')
            s=s+str(solution[i]%(k*k))+''
        else:
            print(k*k,end='')
            s=s+str(k*k)+''
        count=count+1
        if(count%(k*k)==0):
            print('')
            s=s+'\n'
        else:
            print(',',end='')
            s=s+','
with open("MaximalPairSolution.csv", "w") as text_file:
    text_file.write(s)