import stockInfo
from  myModule import myIO
import pandas as pd
from tqdm import tqdm
import config
import granger

@myIO.timer
def mat2edge(Q):
    # Q 矩阵转成边和节点
    # 由于有涨停股票，所以该类股票收益率后期一直是0，和其他股票收益率相关性很大
    cdlist=myIO.loadVar(config.getCdlistPath())
    returnMat=myIO.loadVar(config.getReturnMatPath())

    n = len(Q)
    cdlistPath=config.getCdlistPath()
    cds=myIO.loadVar(cdlistPath)
    names=stockInfo.getNamesBycds(cds)

    source=[]
    target=[]
    weight=[]

    id=[]
    label=[]

    for i in tqdm(range(n)):
        for j in range(i,n):
            ret1=returnMat[:,i]
            ret2=returnMat[:,j]
            if abs(Q[i][j])<abs(Q[j][i]) and granger.granger(ret2,ret1):
                source.append(cds[j])
                target.append(cds[i])
                weight.append(abs(Q[j][j]))
            elif abs(Q[i][j])>abs(Q[j][i]) and granger.granger(ret1,ret2):
                source.append(cds[i])
                target.append(cds[j])
                weight.append(abs(Q[i][j]))
        id.append(cds[i])
        label.append(names[i])
    edges={
        'source':source,
        'target':target,
        'weight':weight
    }
    nodes={
        'id': id,
        'label': label
    }

    pd.DataFrame(nodes).to_excel(config.getNodesPath())
    print('nodes have been saved!')
    pd.DataFrame(edges).to_excel(config.getEdgesPath())
    print('edges have been saved!')

if __name__=='__main__':
    QMatPath=config.getQMatPath()
    Q=myIO.loadVar(QMatPath)
    mat2edge(Q)


