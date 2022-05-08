# 天级别的Q处理
# TODO 天级别的代码还没适配好 先不做天级 把分钟级别的 全体和分板块做好
from myModule import myIO, sqlCmd
from tqdm import tqdm
import os
import stockInfo
import numpy as np
import threading
import pandas as pd
import config
@myIO.timer
def getReturnMat(mkt:tuple):
    indname=config.get('indname')

    # 多个股票在某一天的T(48)个时间段的收益率 矩阵
    outPath=config.getReturnMatPath('day')
    cdlist=[]
    if not os.path.exists(outPath):
        stockcd = stockInfo.getNormalStock(mkt,indname)[0]
        # 各个股票1天48个时间段之间的对数收益率
        returnMat = np.zeros(shape=(304, len(stockcd))) # T*n
        index=0
        for cd in tqdm(stockcd):
            sql=f'''
            select lnreturn from stockprice
            where stkcd={cd}
            '''
            retlst=[i[0] for i in sqlCmd.select(sql)]
            if len(retlst)==304:
                cdlist.append(cd)
                col=np.array(retlst).reshape( (len(retlst),1) ) # 列向量
                returnMat[:,[index]] =col
                index+=1
            else:
                print(f'{cd}数据库中没有交易记录')
        # 剔除全0列
        idx = np.argwhere(np.all(returnMat[..., :] == 0, axis=0))
        returnMat = np.delete(returnMat, idx, axis=1)

        # 保存收益率矩阵变量
        myIO.dumpVar(returnMat, outPath)
        # 保存有交易记录的股票代码list变量
        cdlistPath = config.getCdlistPath()
        myIO.dumpVar(cdlist, cdlistPath)
    else:
        print(f'{outPath}已存在,如需更新请删掉文件，重新运行代码')

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
    assert end<=48*2,f'交易时间不能超过{48*2}个单位'
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


# Q的直方图
@myIO.timer
def plotQ(Q,QMatPath):

    m=np.mean(Q)
    sigma=np.std(Q)
    print(f'q均值{m:.6f},σ={sigma:.6f}')
    plt.figure(dpi=800)
    outPath=f'out/pic/min/'
    plt.hist(Q.flatten(), bins=500, facecolor="blue", alpha=0.5)
    plt.title(myIO.getFileNameExt(QMatPath))
    plt.ylabel('相关性系数')
    plt.xlabel('个数')
    plt.savefig(f'{outPath}{myIO.getFileNameExt(QMatPath).split(".")[0]}.png')


# 对于不同的τ，Q矩阵的q值降序排序
from random import sample
@myIO.timer
def plotQtao():

    plt.figure(dpi=800)
    # TODO 对于不同的tao 可以统计基础的统计变量，比如均值和方差，然后假设检验u1>u2
    for tau in [0,1,2,3,5,6,10]:
        start = 0
        t = 38*2
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
    outPath = f'out/pic/min/'
    plt.title('不同τ的相关性曲线')
    plt.savefig(f'{outPath}不同τ的相关性曲线.png')


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

# 保存了收益率矩阵 cd列表
getReturnMat(mkt)


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

Q=Q.values
plotQ(Q,QMatPath)
plotQtao()








