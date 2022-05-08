'''
json配置文件暂时不熟，用dict偷懒替代一下
'''

global _config
_config = {'mkt':(1),
           'start':0,
           't':47,
           'tau':1,
           'type':'min',
           'indname':'工业',
           }

mkt=_config.get('mkt')
indname=_config.get('indname')
start=_config.get('start')
t=_config.get('t')
tau=_config.get('tau')
T= t + tau
end=T+start


rootPath='src/var/min/'
rootPath='src/var/day/'

def set(key, value):
    _config[key] = value


def get(key):
    return _config.get(key, None)

def get_items():
    return _config.items()

def getCdlistPath():
    cdlistPath=f'src/var/cd-m{mkt}s{start}t{t}tao{tau}{indname}.pkl'
    return cdlistPath

def getReturnMatPath(type=get('type')):
    assert type in ['min','day'],'只允许min day'
    returnMatPath = f'src/var/{type}ReturnMat{mkt}{indname}.pkl'
    return returnMatPath

def getQMatPath(tau=get('tau')):
    QMatPath = f'src/var/Qm{mkt}s{start}e{end}tau{tau}{indname}.pkl'
    return QMatPath