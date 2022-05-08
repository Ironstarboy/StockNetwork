from myModule import sqlCmd,myIO
import stockInfo
import config
import pandas as pd
from tqdm import tqdm
@myIO.timer
def f():
    cd=600001
    mkt=config.get('mkt')
    indname=config.get('indname')
    stockcd = stockInfo.getNormalStock(mkt,indname)[0]
    days=('2021-03-01','2021-03-02','2021-03-03')

    sql=f'''select cd,lnreturn from mindata2
            where trdate in {days} 
                '''
    res=sqlCmd.select(sql)
    col=['stkcd','lnreturn']
    df = pd.DataFrame(list(res),columns=col)
    for cd in tqdm(stockcd):
        retlist=df[df.stkcd==cd]
        print(cd)

f()