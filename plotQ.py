from myModule import myIO
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os
import config

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



# 设置matplotlib正常显示中文和负号
matplotlib.rcParams['font.sans-serif']=['SimHei']   # 用黑体显示中文
matplotlib.rcParams['axes.unicode_minus']=False     # 正常显示负号