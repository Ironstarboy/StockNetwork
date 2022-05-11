# 分钟级别的Q处理
from myModule import myIO, sqlCmd
from tqdm import tqdm
import os
import stockInfo
import numpy as np
# import threading
import pandas as pd
import config

def myCov(A,D):
    # E[ (A-EA)(D-ED) ]
    AMean = np.average(A, axis=1).reshape((A.shape[0], 1))  # 按行求均值,得到n*1的矩阵
    DMean = np.average(D, axis=0).reshape((1, D.shape[1]))  # 按列求均值,得到1*n的矩阵
    t = A.shape[1]  # A:n*t D:t*n
    res = np.dot(A, D) / t - np.dot(AMean, DMean)
    return res


@myIO.timer
def saveQMat(returnMat, filePath, start=0, end=48, tao=1):
    # returnMat T * N
    # 初始Q矩阵，不做绝对值对比
    T=config.get('T')
    assert end<=T,f'交易时间不能超过{T}个单位'
    if not os.path.exists(filePath):
        returnMat=returnMat[start:end,:]
        T=end-start
        t = T - tao
        a = returnMat[:t, :].T # n*t
        d = returnMat[tao:, :] # t*n
        cov = myCov(a,d)
        varA = np.diag(np.cov(a)).reshape((a.shape[0],1)) # 列向量
        varD=np.diag(np.cov(d.T)).reshape((d.shape[1],1))
        omega=np.dot(varA,varD.T)
        omega = omega ** (-0.5)
        res = cov * omega
        myIO.dumpVar(res, filePath)
        print(f'{filePath} saved')
    else:
        print(f'{filePath}已存在,如需更新请删掉文件，重新运行代码')




# 对于不同的τ，Q矩阵的q值降序排序
from random import sample
@myIO.timer
def plotQtao():
    Delta_t = config.get('Delta_t')
    indname=config.get('indname')
    plt.figure(dpi=800)
    days=config.get('days')
    # TODO 对于不同的tao 可以统计基础的统计变量，比如均值和方差，然后假设检验u1>u2
    for tau in [0,1,2,3,5,6,10]:
        start = 0
        t = 48*len(days)-10 # 不同Delta_t需要修改
        T = t + tau
        end = T + start
        # 这边的Q要处理一下
        QMatPath = config.getQMatPath(tau)
        saveQMat(returnMat, QMatPath, start, end, tao=tau)
        Q :np.ndarray= myIO.loadVar(QMatPath)
        m=np.nanmean(Q)
        Q = pd.DataFrame(Q)
        Q.fillna(value=m,inplace=True,axis=1)
        Q=Q.values
        plt.ylabel('相关性系数')
        plt.xlabel('q的序号')
        plt.ylim(0, 1)
        x=sorted(sample(list(map(lambda x:abs(x),Q.flatten())),10000),reverse=1)
        plt.plot(x,label=f'{tau}',linewidth=0.5)
    plt.legend()
    plt.title(f'Delta_t={Delta_t}时不同τ的相关性曲线')

    outPath = f'out/pic/{Delta_t}'
    myIO.mkDir(outPath)
    plt.savefig(f'{outPath}/Delta_t={Delta_t}时不同τ的相关性曲线-{indname}.png')


import matplotlib.pyplot as plt
import matplotlib

# 设置matplotlib正常显示中文和负号
matplotlib.rcParams['font.sans-serif']=['SimHei']   # 用黑体显示中文
matplotlib.rcParams['axes.unicode_minus']=False     # 正常显示负号


mkt=config.get('mkt')
indname=config.get('indname')
start=config.get('start')
t=config.get('t')
tau=config.get('tau')

T= t + tau
end=T+start


returnMatPath=config.getReturnMatPath()
returnMat= myIO.loadVar(returnMatPath)

QMatPath=config.getQMatPath()
saveQMat(returnMat, QMatPath, start, end, tao=tau)

Q:np.ndarray=myIO.loadVar(QMatPath)
m=np.nanmean(Q)
Q=pd.DataFrame(Q)

Q.fillna(value=m,inplace=True,axis=1)
# print(Q[Q.isnull().any()])
# print(Q[Q.isnull().T.all()])


# 绘制Q的相关图
Q=Q.values# df转为ndarray
plotQtao()







