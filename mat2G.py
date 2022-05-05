import stockInfo
from  myModule import myIO
import pandas as pd
from tqdm import tqdm


@myIO.timer
def filterQ(Q,delta=0.5):
    n=len(Q)
    for i in tqdm(range(n)):
        for j in range(n):
            Q[i][j]=abs(Q[i][j])
            Q[j][i]=abs(Q[j][i])
            if Q[i][j]>Q[j][i] :
                Q[j][i]=0
            elif Q[i][j]<Q[j][i]:
                Q[i][j]=0
            else:
                Q[i][j]=Q[j][i]=0
    return Q

qpath='src/var/Qm1s0e48tao1.pkl'
Q=myIO.loadVar(qpath)

@myIO.timer
def mat2edge(Q):
    # Q 矩阵转成边和节点
    # 由于有涨停股票，所以该类股票收益率后期一直是0，和其他股票收益率相关性很大
    n = len(Q)
    col=['source','target','id','label','weight']
    cds=stockInfo.getNormalStock((1))[0]
    names=stockInfo.getNormalStock((1))[1]
    s=[]
    t=[]
    w=[]

    id=[]
    label=[]

    for i in tqdm(range(n)):
        for j in range(n):
            if abs(Q[i][j])<abs(Q[j][i]):
                s.append(cds[j])
                t.append(cds[i])
                w.append(abs(Q[j][j]))
            elif abs(Q[i][j])>abs(Q[j][i]):
                s.append(cds[i])
                t.append(cds[j])
                w.append(abs(Q[i][j]))

            id.append(cds[i])
            id.append(cds[j])
            label.append(names[i])
            label.append(names[j])
    edges={
        'source':s,
        'target':t,
        'weight':w
    }
    nodes={
        'id': id,
        'label': label
    }

    # pd.DataFrame(nodes).to_excel('src/min-Q-nodes.xlsx')
    pd.DataFrame(edges).to_excel('src/min-Q-edges.xlsx')

mat2edge(Q)


