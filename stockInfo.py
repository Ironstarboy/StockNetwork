from myModule import sqlCmd


# 交易日天数
def getNormalStock(mkt:tuple)->list:
    sql=f'''
    select distinct s.stkcd,c.stkname from stockprice s,coinfo c
            where s.markettype in ({mkt})
            and s.stkcd=c.stkcd
            group by s.stkcd
            having count(s.Trdsta=1)=304;
    '''
    res= sqlCmd.select(sql)
    stockCd=[i[0] for i in res]
    name=[i[1] for i in res]
    return stockCd,name






