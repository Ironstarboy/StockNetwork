# Granger因果关系检验
from myModule import myIO
import pandas as pd
from statsmodels.tsa.stattools import grangercausalitytests

def granger(ret1,ret2):
    # ret2是延后的
    a=ret1.tolist()
    b=ret2.tolist()
    d={
        'ret1':a,
        'ret2':b
    }
    df=pd.DataFrame(d)
    res=grangercausalitytests(df[['ret2', 'ret1']], maxlag=1,verbose=False)
    p1=res.get(1)[0].get('ssr_ftest')[1]
    p2=res.get(1)[0].get('ssr_chi2test')[1]
    p3=res.get(1)[0].get('lrtest')[1]
    p4=res.get(1)[0].get('params_ftest')[1]
    # 所有的p小于0.05才能证明b对a有效
    if p1<0.05 and p2<0.05 and p3<0.05 and p4<0.05:
        return 1
    return 0