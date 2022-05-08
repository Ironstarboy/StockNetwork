'''
json配置文件暂时不熟，用dict偷懒替代一下
'''

global _config
_config = {'mkt':(1),
           'start':0,
           't':48*3-1,
           'tau':1,
           'Delta_t':'5min',
           'indname':'工业',
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

def getReturnMatPath(Delta_t=Delta_t):
    assert Delta_t in ['5min','10min','day'],"只允许['5min','10min','day']"
    returnMatPath = f'src/var/{Delta_t}/ReturnMat{mkt}{indname}.pkl'
    return returnMatPath

def getQMatPath(tau=get('tau')):
    QMatPath = f'src/var/{Delta_t}/Qm{mkt}s{start}e{end}tau{tau}{indname}.pkl'
    return QMatPath

