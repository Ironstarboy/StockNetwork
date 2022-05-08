from myModule import sqlCmd
from myModule import myIO
import config

# 交易日天数
def getNormalStock(mkt:tuple,indname:str='')->list:
    # TODO
    if indname=='':
        sql=f'''
        select distinct s.stkcd,c.stkname from stockprice s,coinfo c
                where s.markettype in ({mkt})
                and c.stkname not like '%ST%'
                and s.stkcd=c.stkcd
                group by s.stkcd
                having count(s.Trdsta=1)=304;
        '''
        res= sqlCmd.select(sql)
        stockCd=[i[0] for i in res]

        # stCodesIndex=[127,204,249,261,296,428,729] # 停牌一天
        # stCodes=[stockCd[i] for i in stCodesIndex]
        # for cdindex in stCodes:
        #     stockCd.remove(cdindex)
        # # print(stCodes)
        name=[i[1] for i in res]
        return stockCd,name
    else:
        assert indname in ['金融','公用事业','房地产','综合','工业','商业'],f'{indname}不是合法行业名称'
        sql=f'''
        select distinct s.stkcd,c.stkname from stockprice s,coinfo c
                where s.markettype in ({mkt})
                and c.stkname not like '%ST%'
                and s.stkcd=c.stkcd
                and c.indnme="{indname}"
                group by s.stkcd
                having count(s.Trdsta=1)=304;
        '''
        res = sqlCmd.select(sql)
        stockCd = [i[0] for i in res]

        name = [i[1] for i in res]
        return stockCd, name

@myIO.timer
def getNamesBycds(cdlist:list):

    cdlist=tuple(cdlist)
    sql=f'''
    select stkname from coinfo where stkcd in {cdlist}
    '''

    res=sqlCmd.select(sql)
    names = [i[0] for i in res]
    return names










