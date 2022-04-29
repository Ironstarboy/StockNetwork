import baostock as bs
import pandas as pd
from myModule import sqlCmd
from sqlalchemy import create_engine


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
    rs = bs.query_history_k_data_plus(f"sh.{cd}",
        "date,time,code,open,close",
        start_date='2021-01-04', end_date='2022-01-30',
        frequency="5", adjustflag="3")
    assert rs.error_code=='0',rs.error_msg
    
    data:pd.DataFrame=rs.get_data()

    # 建立连接，username替换为用户名，passwd替换为密码，test替换为数据库名
    # TODO 数据库链接暂时出问题
    connect = create_engine("mysql+pymysql://root:123123@localhost:3306/stockdata")
    # https://www.jianshu.com/p/d34cfe23d5a4
    data.rename(columns={'date': 'trdate',
                         'time': 'trtime',
                         'code': 'cd',
                         'open':'openprice',
                         'close':'closeprice'}, inplace=True)
    data.to_sql( "mindata", connect,if_exists='append',index=False)


import stockInfo
from tqdm import tqdm
def cds2sql():
    login()
    cds=stockInfo.getNormalStock(1)[0]
    for cd in tqdm(cds):
        cd2sql(cd)
    bs.logout()

cds2sql()