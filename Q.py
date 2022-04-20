import myIO
import sqlCmd
from tqdm import tqdm
import os
import stockInfo
import numpy as np


# TODO 忘记对数收益率是怎么写入数据库的了


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
def saveQMat(returnMat, mkt, tao=1):
    # returnMat T * N
    # 初始Q矩阵，不做绝对值对比
    outPath=f'src/var/Q{mkt}.pkl'
    if not os.path.exists(outPath):
        t = returnMat.shape[0] - tao
        a = returnMat[:t, :].T # n*t
        d = returnMat[tao:, :] # t*n
        cov = myCov(a,d)
        varA = np.diag(np.cov(a)).reshape((a.shape[0],1)) # 列向量
        varD=np.diag(np.cov(d.T)).reshape((d.shape[1],1))
        omega=np.dot(varA,varD.T)
        omega = omega ** (-0.5)
        res = cov * omega
        myIO.dumpVar(res,outPath)
    else:
        print(f'{outPath}已存在,如需更新请删掉文件，重新运行代码')


mkt=(1)
getReturnMat(mkt)
returnMat=myIO.loadVar(f'src/var/returnMat{mkt}.pkl')

saveQMat(returnMat, mkt, tao=1)
Q=myIO.loadVar(f'src/var/Q{mkt}.pkl')

def QfFilter(Q,delta):
    ...














