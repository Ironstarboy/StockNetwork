# 做有向复杂网络分析

import myIO
import sqlCmd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib as mpl

plt.rcParams["font.sans-serif"]=["SimHei"] #设置字体
plt.rcParams["axes.unicode_minus"]=False #该语句解决图像中的“-”负号的乱码问题

mkt=1
QMat=myIO.loadVar('src/var/Q{}.pkl'.format(mkt))

@myIO.timer
def QView():
    # 为什么变成正态了？，之前是0超级多，然后+-0.1那边几乎每天，+-0.2那边又有高峰（数值表示目测）
    # TODO 做收益率的可视化、相关性过滤，网络的统计数据输出
    global QMat
    cov=[ QMat[i][j] for i in range(len(QMat)) for j in range(len(QMat))]
    plt.hist(cov,bins=100, alpha=0.5, histtype='stepfilled',
         color='steelblue', edgecolor='none')
    plt.title(f'Q{mkt}')
    plt.show()
QView()




def getNodes():
    global mkt
    nodes=getStockCdName(mkt)[0]
    return nodes


def getEdgesWeight():
    global mkt
    edges=[]
    cd=getStockCdName(mkt)[0]
    for i in range(len(QMat)):
        for j in range(len(QMat)):
            t=(cd[i],cd[j],QMat[i][j])
            edges.append(t)
    return edges


def creatNet():
    DG = nx.DiGraph()
    nodes=getNodes()
    edges=getEdgesWeight()
    DG.add_nodes_from(nodes)
    DG.add_weighted_edges_from(edges)
    return DG

# myIO.dumpVar(creatNet(),'DG.pkl')

import random
def plotG():
    DG=myIO.loadVar('DG.pkl')
    pos = nx.spring_layout(DG)
    nx.draw(DG,
            pos=pos,
            with_labels=True,
            width=[d['weight']*20 for (u,v,d) in DG.edges(data=True)]
            )

    # nx.draw_networkx_nodes(
    #     DG,
    #     pos,
    #     node_size=300,
    #     with_labels=True
    # )
    #
    # elarge = [(u, v) for (u, v, d) in DG.edges(data=True) if d['weight'] > 0.05]
    # esmall = [(u, v) for (u, v, d) in DG.edges(data=True) if d['weight'] <= 0.05]
    # nx.draw_networkx_edges(
    # DG,
    # pos,
    # width=[d['weight']*20 for (u,v,d) in DG.edges(data=True)],
    # alpha=0.5,
    # edge_color='b',
    # with_labels=True,
    # font_size=20
    # )
    #
    # # nx.draw_networkx_edge_labels(
    # #     DG,
    # #     pos
    # # )

    plt.show()

# plotG()

