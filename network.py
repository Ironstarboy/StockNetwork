# 做有向复杂网络分析
from myModule import myIO
import networkx as nx
import matplotlib.pyplot as plt
import stockInfo
# 无向图网络
# 从无向图聚类，发现一些关联股票社群。然后这有什么意义？ 概念股？
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
                # 这边的edge也可以用股票代码或者股票名字替代
                edges.append(edge)
        return edges


    def creatNet(self):
        G=nx.Graph()

        nodes=self.cdName[0]
        G.add_nodes_from(nodes)

        edges=self.getEdges()
        G.add_edges_from(edges)
        return G

    def plotG(self):
        ...