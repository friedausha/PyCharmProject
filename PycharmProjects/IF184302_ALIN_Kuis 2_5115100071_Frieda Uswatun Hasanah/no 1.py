import numpy as np
print('Masukkan jumlah vector dan dimensinya')
row=list(map(int,input().split()))
b=[]
for i in range(0,row[0]):
    a=list(map(int,input().split()))
    b.append(a)
print(b)
b = np.array(b)
det = np.linalg.det(b)
if(det == 0):
    print('linearly dependent')
elif row[0] != row[1]:
    print('doesnt span Rn')
else:
    print('form basis Rn')