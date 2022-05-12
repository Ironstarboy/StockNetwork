import config
import os
import numpy as np
import stockInfo
import pandas as pd
from myModule import  sqlCmd,myIO
from tqdm import tqdm

def getReturnMat(mkt:tuple):
    indname=config.get('indname')
    # 多个股票在某一天的T(48)个时间段的收益率 矩阵
    outPath=config.getReturnMatPath()
    cdlist=[]
    if not os.path.exists(outPath):
        stockcd = stockInfo.getNormalStock(mkt,indname)[0]
        # 各个股票1天48个时间段之间的对数收益率
        days = config.get('days')
        dayLen=48 # 不同min需要修改 5min 48,15min 16 day 304
        returnMat = np.zeros(shape=(dayLen*len(days), len(stockcd))) # T*n
        index=0
        query=f'''
        select cd,lnreturn from {config.Delta_t}data
            where trdate in {days}
        '''
        res=sqlCmd.select(query)
        df=pd.DataFrame(list(res),columns=['stkcd','lnreturn'])
        for cd in tqdm(stockcd):
            retlst:np.ndarray=df[df.stkcd==f'sh.{cd}'].lnreturn.values
            if len(retlst)==dayLen*len(days):
                cdlist.append(cd)
                col=np.array(retlst).reshape( (len(retlst),1) ) # 列向量
                returnMat[:,[index]] =col
                index+=1
            else:
                print(f'{cd}数据库中没有交易记录')
        # 剔除全0列
        idx = np.argwhere(np.all(returnMat[..., :] == 0, axis=0))
        returnMat = np.delete(returnMat, idx, axis=1)
        # 收益率全都×100 变成百分比的收益率
        returnMat=returnMat*100
        # 保存收益率矩阵变量
        myIO.dumpVar(returnMat, outPath)
        # 记录有交易记录的股票代码list变量
        cdlistPath = config.getCdlistPath()
        myIO.dumpVar(cdlist, cdlistPath)
    else:
        print(f'{outPath}已存在,如需更新请删掉文件，重新运行代码')
if __name__=="main__":
    mkt=config.get('mkt')
    getReturnMat(mkt)