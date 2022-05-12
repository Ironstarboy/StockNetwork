# 理论参考文章https://blog.csdn.net/brucewong0516/article/details/81480507

from myModule import sqlCmd,myIO
import stockInfo
import config
from tqdm import tqdm
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt
import matplotlib
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import numpy as np
import pandas as pd
# 设置matplotlib正常显示中文和负号
matplotlib.rcParams['font.sans-serif']=['SimHei']   # 用黑体显示中文
matplotlib.rcParams['axes.unicode_minus']=False     # 正常显示负号

def getRet(cdIndex):
    returnMat=myIO.loadVar(config.getReturnMatPath()) # T*n
    ret=returnMat[:,cdIndex]
    return  ret

# 时序图
def plotTs(ts, stkcd):
    plt.figure(dpi=600)
    plt.plot(ts)
    title=f'{stkcd}收益率序列'
    plt.title(title)
    plt.savefig(f'out/pic/{title}.png')

# acf
def plotAcf(ret,stkcd):
    plt.figure(dpi=600)
    acf=plot_acf(ret)
    acf.savefig(f'out/pic/{stkcd}acf.png')


def plotPacf(ret,stkcd):
    plt.figure(dpi=600)
    pacf = plot_pacf(ret)
    pacf.savefig(f'out/pic/{stkcd}pacf.png')
# 平稳性检验 adf检验


def adf(ret):
    yarn_result = adfuller(ret)  # 生成adf检验结果
    value=yarn_result[0] # Test Statistic Value
    p=yarn_result[1] # p值
    lags=yarn_result[2] # 阶数 Lags Used
    numbers=yarn_result[3]
    # print(f'adf Statistic value {value:.6f}')
    # print(f'p-values {p}')
    # print(f'Lags Used {lags}')
    # print(f'numbers of observation used {numbers}')
    return p

@myIO.timer
def getNotStionarycd():

    cdlist=myIO.loadVar(config.getCdlistPath())
    notStaionaryCd=[]
    for cdIndex in tqdm(range(len(cdlist))):
        ret=getRet(cdIndex)
        p=adf(ret)
        if p>0.1:
            notStaionaryCd.append(cdlist[cdIndex])
    return notStaionaryCd


# 单个股票的基本信息输出
def singleCdInfo(stkcd):
    cdlist=myIO.loadVar(config.getCdlistPath())
    cdIndex=cdlist.index(stkcd)
    ret=getRet(cdIndex)
    plotAcf(ret,stkcd)
    plotPacf(ret,stkcd)
    plotTs(ret,stkcd)



def fileterNotStaionaryStock():
    cdlist = myIO.loadVar(config.getCdlistPath())
    notStaionaryCd = getNotStionarycd()
    # returnMat去除非平稳的股票
    returnMat = myIO.loadVar(config.getReturnMatPath())
    notStaionaryCdIndex = []
    for cd in notStaionaryCd:
        cdIndex = cdlist.index(cd)
        notStaionaryCdIndex.append(cdIndex)
    returnMat = np.delete(returnMat, notStaionaryCdIndex, axis=1)
    myIO.loadVar(config.getReturnMatPath())

    for cd in notStaionaryCd:
        cdlist.remove(cd)
    myIO.dumpVar(cdlist, config.getCdlistPath())


if __name__=="__main__":
    fileterNotStaionaryStock()

    # singleCdInfo(600533)

