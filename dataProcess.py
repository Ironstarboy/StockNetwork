import myIO
import sqlCmd

# 存在有的股票在某一天不交易的情况，缺失值补0

#所有的交易日
# allDate=[i[0] for i in sqlCmd.select('select distinct trddt from stockprice')]
# 所有的股票代码
tao=1

def getAllStockcd(mkt):
    stockCd=[i[0] for i in sqlCmd.select('select distinct Stkcd from stockprice where Markettype={}'.format(mkt))]
    return stockCd

# 存在一些股票 刚刚上市 交易日期太晚。那么就找到股票ab都交易的天数，开始计算相关系数

def findSTStock():
    # 过滤交易日期少于50天的
    # 去除很多ST的
    sql='select stkcd from stockprice group by stkcd having count(Trdsta=1)<200 '
    stockcds=[i[0] for i in sqlCmd.select(sql)]
    return stockcds

def getNormalStock(mkt):

    STStock=findSTStock()
    allStockcd=getAllStockcd(mkt)
    stockCd=[i for i in allStockcd if i not in STStock ]
    return stockCd


import numpy as np
def Q(cd1:int,cd2:int):
    global tao
    # 返回股票a b的关联系数q。先采用陈花提出的计算方法
    # deltaT=1d

    # 共同交易日的收益率序列
    sql='''select s1.lnreturn,s2.lnreturn 
        from stockprice s1,stockprice s2
        where s1.trddt=s2.trddt
        and s1.stkcd={}
        and s2.stkcd={}'''.format(cd1,cd2)
    ret1=[i[0] for i in sqlCmd.select(sql)]
    ret2=[i[1] for i in sqlCmd.select(sql)]

    if len(ret1)!=len(ret2):
        raise Exception
    mean1=np.mean(ret1[:len(ret1)-tao])
    std1=np.std(ret1[:len(ret1)-tao])

    mean2=np.mean(ret2[:len(ret2)-tao])
    std2=np.std(ret2[:len(ret2)-tao])

    s=0
    for k in range(len(ret1)-tao):
        s+=ret1[k]*ret2[k+tao]
    s=s/(len(ret1)-tao)
    qIJ=(s-mean1*mean2)/(std1*std2)
    return qIJ



import os
from tqdm import tqdm

def saveQMat(filePath,mkt):
    global tao
    if not os.path.exists(filePath):
        QMat=[]
        stockCd = getNormalStock(mkt)
        print('saving markeytype{} var Q{}'.format(mkt,mkt))
        for i in tqdm(range(len(stockCd))):
            row=[0]*len(stockCd)
            cd1=stockCd[i]
            # 相关性矩阵是对称的,不是对称的
            for j in range(len(stockCd)):
                cd2=stockCd[j]
                row[j]=Q(cd1,cd2)
            QMat.append(row)
        myIO.dumpVar(QMat,filePath)
    else:
        print('{}已存在\n若想更新，请删除原数据'.format(filePath))

def insertQ(mkt):
    global tao
    stockCd = getNormalStock(mkt)
    print(f'saving markeytype{mkt} var Q{mkt} into sql table Q{mkt}')

    sqlCmd.create(f'''
    create table Q{mkt}(
        stkcd1 int,
        stkcd2 int,
        cov double ,
        primary key (stkcd1,stkcd2)
    );
    ''',f'Q{mkt}')
    for i in tqdm(range(len(stockCd))):
        cd1 = stockCd[i]
        for j in range(len(stockCd)):
            cd2 = stockCd[j]
            sqlCmd.insert(f'''
            insert into Q{mkt}
            value ({cd1},{cd2},{Q(cd1,cd2)})
            ''')


def QFilter(delta):
    global QMat
    global mkt
    n = len(QMat)
    tableName=f'q{mkt}filtered'
    sqlCmd.create(f'''
    create table {tableName}(
        stkcd1 int,
        stkcd2 int,
        cov double ,
        primary key (stkcd1,stkcd2)
)
''')
    for i in range(n):
        for j in range(n):
            if abs(QMat[i][j]) > abs(QMat[j][i]) and abs(QMat[i][j])>delta:
                sqlCmd.insert(f'insert into {tableName} value ({QMat[i][j]}')
            elif abs(QMat[i][j]) < abs(QMat[j][i]) and abs(QMat[j][i])>delta:
                sqlCmd.insert(f'insert into {tableName} value ({QMat[j][i]}')

QFilter(0.02)




















