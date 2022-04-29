from myModule import myIO
from myModule import sqlCmd

mkt=(1)
start=0
t=304
tao=30
T=t+tao
end=T+start

def p_acf(ret,stkcd):
    from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
    acf=plot_acf(ret)
    pacf=plot_pacf(ret)
    acf.savefig(f'out/pic/{stkcd}acf.png')
    pacf.savefig(f'out/pic/{stkcd}pacf.png')

def getRet(stkcd=601658):
    global start
    global end
    sql = f'''
           select lnreturn from stockprice where
           stkcd={stkcd} 
           '''
    ret= [i[0] for i in sqlCmd.select(sql)][start:end]
    return  ret

import stockInfo
from statsmodels.tsa.stattools import adfuller
from tqdm import tqdm
@myIO.timer
def adf():
    global mkt
    # p值为零，说明是拒绝原假设，表明该序列是一个平稳序列。
    stockcd=stockInfo.getNormalStock(mkt)[0]
    notStationaryCd=[]
    for cd in tqdm(stockcd):
        ret=getRet(cd)
        yarn_result = adfuller(ret)  # 生成adf检验结果
        p=yarn_result[1]
        if p>0.05:
            notStationaryCd.append(cd)
    return notStationaryCd
    # print('The ADF Statistic of ret: %f' % yarn_result[0])
    # print('The p value of ret: %f' % yarn_result[1])

res=adf()
