import stockInfo
from  myModule import myIO
import pandas as pd
from tqdm import tqdm
import config

#
@myIO.timer
def filterQ(Q):
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

QMatPath=config.getQMatPath()
# qpath='src/var/Qm1s0e48tao1.pkl'
Q=myIO.loadVar(QMatPath)


@myIO.timer
def mat2edge(Q):
    # Q 矩阵转成边和节点
    # 由于有涨停股票，所以该类股票收益率后期一直是0，和其他股票收益率相关性很大
    n = len(Q)
    col=['source','target','id','label','weight']

    cdlistPath=config.getCdlistPath()
    cds=myIO.loadVar(cdlistPath)
    names=stockInfo.getNamesBycds(cds)
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
        label.append(names[i])
    edges={
        'source':s,
        'target':t,
        'weight':w
    }
    nodes={
        'id': id,
        'label': label
    }

    indname=config.get('indname')

    print('saving xlsx...')
    pd.DataFrame(nodes).to_excel(f'src/min-Q-nodes{indname}.xlsx')
    pd.DataFrame(edges).to_excel(f'src/min-Q-edges{indname}.xlsx')

mat2edge(Q)


