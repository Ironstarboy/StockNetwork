from myModule import myIO
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os
import config

# Q的直方图
@myIO.timer
def plotQ():

    df=pd.read_excel(config.getEdgesPath())
    qList=df['weight']

    m=np.mean(qList)
    sigma=np.std(qList)
    print(f'q均值{m:.6f},σ={sigma:.6f}')
    plt.figure(dpi=800)


    plt.hist(sorted(qList,reverse=1), bins=500, facecolor="blue", alpha=0.5)
    title=myIO.getFileNameExt(config.getQMatPath()).replace('.pkl','')
    plt.title(title)
    plt.xlabel('相关性系数')
    plt.ylabel('个数')
    plt.savefig(f'out/pic/{config.Delta_t}/{title}.png')


if __name__=='__main__':
    # 设置matplotlib正常显示中文和负号
    matplotlib.rcParams['font.sans-serif']=['SimHei']   # 用黑体显示中文
    matplotlib.rcParams['axes.unicode_minus']=False     # 正常显示负号

    plotQ()