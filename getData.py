import baostock as bs
import pandas as pd
from myModule import sqlCmd
from sqlalchemy import create_engine

import config
def login():
    #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    assert lg.error_code=='0',lg.error_msg


def cd2sql(cd):

    #### 获取沪深A股历史K线数据 ####
    # 详细指标参数，参见“历史行情指标参数”章节；“分钟线”参数与“日线”参数不同。“分钟线”不包含指数。
    # 分钟线指标：date,time,code,open,high,low,close,volume,amount,adjustflag
    # 周月线指标：date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg
    Delta_t=15
    rs = bs.query_history_k_data_plus(f"sh.{cd}",
        "date,time,code,open,close",
        start_date='2021-03-01', end_date='2021-03-30',
        frequency=f"{Delta_t}", adjustflag="3")
    assert rs.error_code=='0',rs.error_msg

    data:pd.DataFrame=rs.get_data()

    # 建立连接，username替换为用户名，passwd替换为密码，test替换为数据库名
    connect = create_engine("mysql+pymysql://root:123123@localhost:3306/stockdata")
    # https://www.jianshu.com/p/d34cfe23d5a4
    data.rename(columns={'date': 'trdate',
                         'time': 'trtime',
                         'code': 'cd',
                         'open':'openprice',
                         'close':'closeprice'}, inplace=True)
    data.to_sql( f"{Delta_t}mindata", connect,if_exists='append',index=False)
    # mindata 数据库是2021-01-04到2022-01-30的5分钟级数据
    # mindata2数据库是2021-03-01到2021-03-30的5分钟级数据
    # 15mindata是2021-03-01到2021-03-30的15分钟级数据

import stockInfo
from tqdm import tqdm
def cds2sql():
    login()
    cds=stockInfo.getNormalStock(1)[0]
    for cd in tqdm(cds):
        cd2sql(cd)
    bs.logout()

cds2sql()
