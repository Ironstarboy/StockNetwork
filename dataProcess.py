import myIO
import sqlCmd
from tqdm import tqdm
import os
# 存在有的股票在某一天不交易的情况，缺失值补0

#所有的交易日
# allDate=[i[0] for i in sqlCmd.select('select distinct trddt from stockprice')]
# 所有的股票代码
# TODO 忘记对数收益率是怎么写入数据库的了



def getNormalStock(mkt:tuple)->list:
    sql=f'''
    select distinct s.stkcd,c.stkname from stockprice s,coinfo c
            where s.markettype in ({mkt})
            and s.stkcd=c.stkcd
            group by s.stkcd
            having count(s.Trdsta=1)=304;
    '''
    res=sqlCmd.select(sql)
    stockCd=[i[0] for i in res]
    name=[i[1] for i in res]
    return stockCd,name

@myIO.timer
def getReturnMat(mkt:tuple):
    stockcd=getNormalStock(mkt)[0]
    returnMat=np.empty(shape=(304,len(stockcd)))

    outPath=f'src/var/returnMat{mkt}.pkl'

    if not os.path.exists(outPath):
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
        print(f'本地已计算过{outPath},如需更新请删掉文件，重新运行代码')



import numpy as np
@myIO.timer
def calQMat(returnMat,mkt,tao=1):
    outPath=f'src/var/Q{mkt}.pkl'
    if not os.path.exists(outPath):
        t = returnMat.shape[0] - tao
        a = returnMat[:t, :]
        d = returnMat[tao:, :]
        ad = a.T.dot(d)
        cov = np.cov(ad)
        ad = np.diag(cov)
        ad = ad.reshape((len(ad), 1))
        omega = ad * (ad.T)
        omega = omega ** (-0.5)
        res = cov * omega
        myIO.dumpVar(res,outPath)
    else:
        print(f'本地已计算过{outPath},如需更新请删掉文件，重新运行代码')



mkt=(1)
getReturnMat(mkt)
returnMat=myIO.loadVar(f'src/var/returnMat{mkt}.pkl')

calQMat(returnMat,mkt,1)
Q=myIO.loadVar(f'src/var/Q{mkt}.pkl')

























