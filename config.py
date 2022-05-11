'''
json配置文件暂时不熟，用dict偷懒替代一下
此种方式写是不方便的，没法把set的内容持久化记录下
'''

global _config
_config = {'mkt':(1),
           'start':0,
           't':48*2-1,
           'tau':1,
           'Delta_t':'5min',
           'indname':'全行业',
           'days':('2021-03-01', '2021-03-02')
           }

mkt=_config.get('mkt')
indname=_config.get('indname')
start=_config.get('start')
t=_config.get('t')
tau=_config.get('tau')
Delta_t=_config.get('Delta_t')

T= t + tau
end=T+start


def set(key, value):
    _config[key] = value

def get(key):
    if key=='T':
        return T
    return _config.get(key, None)

def get_items():
    return _config.items()

def getCdlistPath():
    cdlistPath=f'src/var/{Delta_t}/cd-m{mkt}s{start}t{t}tau{tau}{indname}.pkl'
    return cdlistPath

def getReturnMatPath():

    assert Delta_t in ['5min','15min','day'],f"{Delta_t} not in ['5min','10min','day']"
    returnMatPath = f'src/var/{Delta_t}/ReturnMat{mkt}{indname}.pkl'
    return returnMatPath

def getQMatPath(tau=get('tau')):
    QMatPath = f'src/var/{Delta_t}/Qm{mkt}s{start}e{end}tau{tau}{indname}.pkl'
    return QMatPath

def getNodesPath():
    nodesPath=f'src/{Delta_t}-Q-nodes-t{t}{indname}.xlsx'
    return nodesPath

def getEdgesPath():
    edgesPath=f'src/{Delta_t}-Q-edges-t{t}{indname}.xlsx'
    return edgesPath
