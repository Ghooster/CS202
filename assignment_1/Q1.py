import numpy as np
from pysat.solvers import Solver

k=int(input("Enter k\n"))
#x[i][j][v] is a boolean variable which stores if the value at ith row, jth column of the first sudoku is v or not. Similarily, for 2nd sudoku we have y.
x=[[[0 for i in range(k*k)] for j in range(k*k)] for v in range(k*k)]
y=[[[0 for i in range(k*k)] for j in range(k*k)] for v in range(k*k)]
for i in range(0,(k*k)):
    for j in range(0,(k*k)):
        for v in range(0,(k*k)):
            x[i][j][v]=((i)*(k**4)) + ((j)*k*k) + v + 1         #Maps x[i][j][v] toa unique integer (((i)*(k**4)) + ((j)*k*k) + v + 1 )
            y[i][j][v]=((i)*(k**4)) + ((j)*k*k) + v + k**6 + 1  #Maps x[i][j][v] toa unique integer (((i)*(k**4)) + ((j)*k*k) + v + k**6 + 1)

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
#Input Constraints
path1=input("Enter path of CSV file\n")
temp=np.genfromtxt(path1, delimiter=',', dtype=int)
temp1=temp[0:k*k]
temp2=temp[k*k:2*k*k]
for i in range(0,k*k):
    for j in range(0,k*k):
        if(temp1[i,j]!=0):
            cnf.append([x[i][j][temp1[i,j]-1]])
        if(temp2[i,j]!=0):
            cnf.append([y[i][j][temp2[i,j]-1]])

s=Solver()
s.append_formula(cnf)
s.solve()
result=s.get_model()

s=''
if result is None:
    print("Sukodu pair is not possible")
else:
    count=0
    print("Sudodu #1:")
    for i in range(0,k**6):
        if(result[i]>0):
            if(result[i]%(k*k)>0):
                print(result[i]%(k*k),end='')
                s=s+str(result[i]%(k*k))+''
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
        if(result[i]>0):
            if(result[i]%(k*k)>0):
                print(result[i]%(k*k),end='')
                s=s+str(result[i]%(k*k))+''
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
with open("Output.csv", "w") as text_file:
    text_file.write(s)