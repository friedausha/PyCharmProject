from sympy import Matrix
import numpy as np
print('Masukkan jumlah vector dan dimensinya')
row=list(map(int,input().split()))
b=[]
for i in range(0,row[0]):
    a=list(map(int,input().split()))
    b.append(a)
print(b)
b = np.array(b)
A = Matrix(b)
print(A.nullspace())