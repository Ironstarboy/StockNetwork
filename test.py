import pandas as pd

import sqlCmd
from tqdm import tqdm
import myIO
import numpy as np
import math
import pandas as pd
import os



def myCov(A,D):
    # E[ (A-EA)(D-ED) ]
    AMean = np.average(A, axis=1).reshape((A.shape[0], 1))  # 按行求均值,得到n*1的矩阵
    AM = np.tile(AMean, (1, A.shape[1]))
    DMean = np.average(D, axis=0).reshape((1, D.shape[1]))  # 按列求均值,得到1*n的矩阵
    DM = np.tile(DMean, (D.shape[0], 1))
    A = A - AM
    D = D - DM
    t = A.shape[1]  # A:n*t D:t*n
    res = np.dot(A, D) / t
    return res


PT=np.array([
    [0,1,0,3],
    [1,0,2,1]
    ]
) # n*T 收益率矩阵
P=PT.T # T*n
tao=1
t=P.shape[0]-tao

a=PT[:,:t]
d=P[tao:,:]
cov=myCov(a,d)
def fenziMat(PT):
    # 分子应该和myCOV一样
    global t
    global tao
    Q=[]
    for i in range(PT.shape[0]):
        row=[0]*PT.shape[0]
        Q.append(row)

    for i in range(len(PT)):
        temp=PT[i:i+1,:t]
        meana=np.mean(PT[i:i+1,0:t]) # a行收益率
        vara=np.var(PT[i:i+1,0:t])
        for j in range(len(PT)):
            tep = PT[j:j + 1, tao:]
            meanb=np.mean(PT[j:j+1,tao:]) # b行收益率
            varb=np.var(PT[j:j+1,tao:])
            u=0
            for k in range(t):
                u+=PT[i,k]*PT[j,k+tao]
            u=u/t-meana*meanb # u i j
            Q[i][j]=u
    return Q

Q=fenziMat(PT)





