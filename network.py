# 做有向复杂网络分析
from myModule import myIO
import networkx as nx
import matplotlib.pyplot as plt
import stockInfo



# 无向图网络
# 从无向图聚类，发现一些关联股票社群。然后这有什么意义？ 概念股？

import stockInfo
class Net():
    def __init__(self,QMat,mkt):
        self.Q=QMat
        self.mkt=mkt
        self.cdName=stockInfo.getNormalStock(mkt) # ([cd],[name])
        self.G=self.creatNet()


    def getEdges(self):
        edges=[]
        cd=self.cdName[0]
        for i in range(len(self.Q)):
            for j in range(len(self.Q)):
                edge=(cd[i],cd[j],self.Q[i][j])
                edges.append(edge)
        return edges


    def creatNet(self):
        G=nx.Graph()

        nodes=self.cdName[0]
        G.add_nodes_from(nodes)

        edges=self.getEdges()
        G.add_edges_from(edges)
        return G

mkt=(1)
start=0
t=303
tao=0
T=t+tao
end=T+start
QMatPath=f'src/var/Qm{mkt}s{start}e{end}tao{tao}.pkl'
Q=myIO.loadVar(QMatPath)
n=Net(Q,mkt)