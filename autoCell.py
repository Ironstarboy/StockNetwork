# 元胞状态：买入 持有 卖出 ，需要考虑量的问题，就是元胞属性多一个持有量
"""
元胞自动机 Python 实现
"""
import numpy as np
import random
import matplotlib.pyplot as plt
from itertools import chain
import matplotlib.animation as animation
import imageio
import my_IO


class Cell:
    def __init__(self,state,x,y):
        # 0
        # 1
        # 2
        self.state = state
        self.x=x
        self.y=y

    def showInfo(self):
        info="({},{}),{}".format(self.x,self.y,self.state)
        print(info,end=' ')

class CellularAutomation:
    HEIGHT=3
    WIDTH=3
    def __init__(self,height=HEIGHT,width=WIDTH):
        self.height=height
        self.width=width
        self.timer=0
        self.cellSpace =[]
        self.historySpace=[]

        # 分别初始化，以保证地址不同。python类里面默认拷贝对象，引用传递了
        for i in range(0,height):
            row=[]
            for j in range(0,width):
                row.append(Cell(random.randint(0,1),i,j))
            self.cellSpace.append(row)

        for i in range(0, height):
            row = []
            for j in range(0, width):
                row.append(Cell(random.randint(0,1), i, j))
            self.historySpace.append(row)

    def mat2np(self):
        # cell矩阵转为numpy矩阵
        self.stateData = []
        for i in range(0, self.height):
            row=[]
            for j in range(0, self.width):
                row.append(self.cellSpace[i][j].state)
            self.stateData.append(row)

        self.stateData=np.array(self.stateData)
        # print(self.stateData)
        return self.stateData


    def countNeighbour(self,currentCell:Cell):
        # 扩展摩尔型邻居
        x=currentCell.x
        y=currentCell.y
        count=0
        for i in range(x-1, x+2):
            for j in range(y-1,y+2):
                if i<0 or i>=self.width or j<0 or j>=self.height:
                    continue
                if not (i==x and j==y) :
                    if self.historySpace[i][j].state==1:
                        count+=1
        return count

    def valueCopy(self,src,target):
        for i in range(0,self.height):
            for j in range(0,self.width):
                target[i][j].x=src[i][j].x
                target[i][j].y = src[i][j].y
                target[i][j].state = src[i][j].state


    def stateUpdate(self):
        # 判断当前元胞的状态，并根据规则更新状态
        # 演化规则
        # p1 风险承担程度
        # p2 风险传然概率
        # p3 风险抵御能力
        # p4 央行救助强度
        self.valueCopy(src=self.cellSpace, target=self.historySpace)
        for i in range(0, self.height):
            for j in range(0, self.width):
                currenCell=self.cellSpace[i][j]
                historyCell=self.historySpace[i][j]
                count=self.countNeighbour(historyCell)
                # 当前元胞活着：只有2or3个邻居活着，下一刻活着
                if currenCell.state==1:
                    if count==2 or count==3:
                        currenCell.state=1
                # 当前元胞活着：一个活着，四个以上活着，下一个死亡
                    else :
                        currenCell.state=0
                # 当前死亡，三个活着，变活
                else:
                    if count==3:
                        currenCell.state=1

        self.valueCopy(src=self.cellSpace, target=self.historySpace)
        self.timer+=1
        self.mat2np()


    def plot(self):
        # 画出当前状态
        plt.title("time {}".format(self.timer))

        plt.imshow(self.stateData)
        plt.show()

    def isEqual(self,old,new):
        flag=1
        for i in range(0, self.height):
            for j in range(0, self.width):
                if self.historySpace[i][j].state!=self.cellSpace[i][j].state:
                    flag=0
                    break
        return flag


    def updateAndPlot(self,nIter):
        # self.mat2np()  # 0时刻
        # print()
        outPicDirPath = 'out\\pic'
        my_IO.mkDir(outPicDirPath)
        my_IO.delFileByDir(outPicDirPath)  # 先删除旧的文件
        pics=[]

        for i in range(nIter):
            self.stateUpdate()

            # print()
            pic=plt.imshow(self.stateData, cmap=plt.cm.hot,
                         vmin=0, vmax=1)
            plt.colorbar()
            plt.grid(True)
            # plt.show()
             # 画完一张重置图
            pics.append(pic)

            plt.savefig('{}\\{}.png'.format(outPicDirPath,i))
            plt.clf()

    def pngs2Gif(self):


        gif_images = []

        fileNameList=my_IO.getFileNameList('out\\pic')
        fileNameList.sort(key=lambda x: int(x[0:x.index('.')])) # 按照数字大小排序，否则按照文字排序会错序
        for fileNameExt in fileNameList:

            gif_images.append(imageio.imread('out\\pic\\'+fileNameExt))  # 读取多张图片
        imageio.mimsave("out\\autocell.gif", gif_images, fps=5)  # 转化为gif动画
        print('gif done')

if __name__=='__main__':
    ca=CellularAutomation( 10,10)
    # ca.plot()
    # ca.updateAndPlot(100)
    ca.pngs2Gif()
