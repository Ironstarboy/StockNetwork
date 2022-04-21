import myIO
import sqlCmd
from tqdm import tqdm
import os
import stockInfo
import numpy as np


# TODO 忘记对数收益率是怎么写入数据库的了,好像是数据库直接Insert的


@myIO.timer
def getReturnMat(mkt:tuple):
    outPath=f'src/var/returnMat{mkt}.pkl'
    if not os.path.exists(outPath):
        stockcd = stockInfo.getNormalStock(mkt)[0]
        # 各个股票304天之间的对数收益率
        returnMat = np.empty(shape=(304, len(stockcd)))
        index=0
        for cd in tqdm(stockcd):
            sql=f'''
            select lnreturn from stockprice
            where stkcd={cd}
            '''
            retlst=[i[0] for i in sqlCmd.select(sql)]
            col=np.array(retlst).reshape( (len(retlst),1) ) # 列向量
            returnMat[:,[index]] =col
            index+=1
        myIO.dumpVar(returnMat,outPath)
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
def saveQMat(returnMat, filePath, start=0, end=304, tao=1):
    # returnMat T * N
    # 初始Q矩阵，不做绝对值对比

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
        myIO.dumpVar(res,filePath)
        print(f'{filePath} saved')
    else:
        print(f'{filePath}已存在,如需更新请删掉文件，重新运行代码')

def QfFilter(Q,delta):
    ...


@myIO.timer
def plotQ(Q,QMatPath):
    sigma=np.std(Q)
    outPath=f'out/pic/'
    plt.hist(Q.flatten(), bins=100, facecolor="blue", alpha=0.5)
    plt.title(myIO.getFileName(QMatPath))
    plt.savefig(f'{outPath}{myIO.getFileName(QMatPath).split(".")[0]}.png')

def p_acf(ret):
    from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
    acf=plot_acf(ret)
    pacf=plot_pacf(ret)
    acf.savefig(f'out/pic/{stkcd}acf.png')
    pacf.savefig(f'out/pic/{stkcd}pacf.png')

import matplotlib.pyplot as plt
import matplotlib

# 设置matplotlib正常显示中文和负号
matplotlib.rcParams['font.sans-serif']=['SimHei']   # 用黑体显示中文
matplotlib.rcParams['axes.unicode_minus']=False     # 正常显示负号


mkt=(1)
start=0
t=90
tao=30
T=t+tao
end=T+start

getReturnMat(mkt)
returnMatPath=f'src/var/returnMat{mkt}.pkl'
returnMat=myIO.loadVar(returnMatPath)

# QMatPath=f'src/var/Qm{mkt}s{start}e{end}tao{tao}.pkl'
# saveQMat(returnMat, QMatPath, start,end,tao=tao)
# Q=myIO.loadVar(QMatPath)
# plotQ(Q,QMatPath)


stkcd=600031
sql = f'''
       select lnreturn from stockprice where
       stkcd={stkcd}
       '''
ret=[i[0] for i in sqlCmd.select(sql)][start:end]
@myIO.timer
def plotRet(ret):
    plt.plot(ret)
    plt.savefig(f'out/pic/{stkcd}ret.png')


from random import sample
@myIO.timer
def plotQtao():
    plt.figure(dpi=600)
    for tao in [0,1,10,20,30]:
        start = 0
        t = 50
        T = t + tao
        end = T + start
        QMatPath = f'src/var/Qm{mkt}s{start}e{end}tao{tao}.pkl'
        saveQMat(returnMat, QMatPath, start, end, tao=tao)
        Q = myIO.loadVar(QMatPath)

        plt.ylim(0, 1)
        plt.plot(sorted(sample(list(map(lambda x:abs(x),Q.flatten())),500),reverse=1),label=f'{tao}',linewidth=0.5)
    plt.legend()
    outPath = f'out/pic/'
    plt.title('不同tao的相关性曲线')
    plt.savefig(f'{outPath}不同tao的相关性曲线.png')

plotQtao()

# plotRet(ret)
# p_acf(ret)








