from myModule import myIO, sqlCmd
from tqdm import tqdm
import os
import stockInfo
import numpy as np

# TODO 忘记对数收益率是怎么写入数据库的了,好像是数据库直接Insert的

@myIO.timer
def getReturnMat(mkt:tuple):
    # 多个股票T 天的收益率 矩阵
    outPath=f'src/var/returnMat{mkt}.pkl'
    if not os.path.exists(outPath):
        stockcd = stockInfo.getNormalStock(mkt)[0]
        # 各个股票304天之间的对数收益率
        returnMat = np.empty(shape=(304, len(stockcd))) # n*T
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
        myIO.dumpVar(returnMat, outPath)
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
    assert end<=304,'交易日不能超过304天'
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

    sigma=np.std(Q)
    outPath=f'out/pic/'
    plt.hist(Q.flatten(), bins=100, facecolor="blue", alpha=0.5)
    plt.title(myIO.getFileName(QMatPath))
    plt.savefig(f'{outPath}{myIO.getFileName(QMatPath).split(".")[0]}.png')


# 对于不同的τ，Q矩阵的q值降序排序
from random import sample
@myIO.timer
def plotQtao():

    plt.figure(dpi=800)
    # TODO 对于不同的tao 可以统计基础的统计变量，比如均值和方差，然后假设检验u1>u2
    for tao in [0,1,2,3,5,10]:
        start = 0
        t = 50
        T = t + tao
        end = T + start
        QMatPath = f'src/var/Qm{mkt}s{start}t{t}tao{tao}.pkl'
        saveQMat(returnMat, QMatPath, start, end, tao=tao)
        Q = myIO.loadVar(QMatPath)

        plt.ylim(0, 0.8)
        plt.plot(sorted(sample(list(map(lambda x:abs(x),Q.flatten())),1000),reverse=1),label=f'{tao}',linewidth=0.5)
    plt.legend()
    outPath = f'out/pic/'
    plt.title('不同tao的相关性曲线')
    plt.savefig(f'{outPath}不同τ的相关性曲线.png')


import matplotlib.pyplot as plt
import matplotlib

# 设置matplotlib正常显示中文和负号
matplotlib.rcParams['font.sans-serif']=['SimHei']   # 用黑体显示中文
matplotlib.rcParams['axes.unicode_minus']=False     # 正常显示负号


mkt=(1)
start=0
t=303
tao=0
T=t+tao
end=T+start
stkcd=600125

getReturnMat(mkt)
returnMatPath=f'src/var/returnMat{mkt}.pkl'
returnMat= myIO.loadVar(returnMatPath)

QMatPath=f'src/var/Qm{mkt}s{start}e{end}tao{tao}.pkl'
saveQMat(returnMat, QMatPath, start,end,tao=tao)
Q=myIO.loadVar(QMatPath)
plotQ(Q,QMatPath)
# plotQtao()








