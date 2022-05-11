# 数据处理步骤

1. 从CSMAR下载excel数据

2. excel导入数据库

   1. 先在数据库中创建表格，写出字段的完整性约束

      ~~~sql
      create table coInfo(
      	stkcd int primary key,
          stkname varchar(20),
          conme varchar(100),
          indnme varchar(20),
          listdt varchar(20),
          statco char(1),
          markettype int,
          PROVINCE varchar(20),
          city varchar(30)
      );
      ~~~

   2. 数据预处理：

      1. excel中包含一些表头和中文，打开excel手中删除，以保证字段数据类型统一。英文表头也要去除
      2. excel保存为csv

   3. 导入数据：

      1. [修改mysql secure-file-pive](https://icode.best/i/42060943545434)
      2. cdm中以root身份链接Mysql stockdata schema，输入以下指令

      ~~~powershell
      mysql -u root -p stockdata
      ~~~

      输入root账户的密码

      输入以下命令，一定要是\\\\转义

      ~~~sql
      -- use stockdata;
      set global local_infile=on;
      show variables like '%secure%';
      SHOW VARIABLES LIKE "secure_file_priv";
      LOAD DATA INFILE "C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\coInfo.csv"
      into table coInfo
      FIELDS TERMINATED BY ',' 
      OPTIONALLY ENCLOSED BY '"' 
      LINES TERMINATED BY '\n';
      ~~~

## 分钟级别数据存储方案

  

# 数据字段说明

Stkcd [证券代码] - 以上交所、深交所公布的证券代码为准
Stknme [证券简称] - 以交易所公布的中文简称为准
Conme [公司全称] - 以公司公布的中文名为准
Indnme [行业名称A] - Finance=金融，Utilities=公用事业，Properties=房地产，Conglomerates=综合，Industrials=工业，Commerce=商业
Listdt [上市日期] - 以YYYY-MM-DD表示，上市日期为此股票证券代码的上市日期.
Statco [公司活动情况] - A=正常交易，D＝终止上市，S=暂停上市， N=停牌
Markettype [市场类型] - 1=上证A股市场 (不包含科创板），2=上证B股市场，4=深证A股市场（不包含创业板），8=深证B股市场，16=创业板， 32=科创板，64=北证A股市场。
PROVINCE [所属省份] - 注册地址所属省份。
CITY [所属城市] - 注册地址所属城市。

# 网络



## 绘图

https://lhyxx.top/2019/10/06/%E7%BB%98%E5%9B%BE%E7%A5%9E%E5%99%A8-networkx/

# 参考教程

networkx绘图：https://lhyxx.top/2019/10/06/%E7%BB%98%E5%9B%BE%E7%A5%9E%E5%99%A8-networkx/#nx-draw-networkx-labels-%E7%94%BB%E7%82%B9%E7%9A%84labels	

# 处理步骤

1. 从csmar下载日级数据，保存交易数据到数据库stockprice coinfo;
   从baostock下载k分钟级交易数据，保存数据到kmindata
   1. baostock用的sqlalchemy把df写入数据库，默认格式都是下载格式的text，需要alter改字段类型
2. 数据库使用update指令，根据收盘价开盘价格计算对数收益率序列
3. 运营retunrnMat.py文件得到收益率序列，记录有交易记录的股票代码list变量；得到指定开始时间、截止时间、市场类型、行业类型的收益率矩阵returnMat。
4. 运行timeSetires.py文件，进行adf检验。去除非平稳序列,得到平稳股票的cdlist。更新retunrnMat
5. 运行minQ.py文件，根据returnmat,计算出Q值。要注意t的值和returnmat的维度
6. 运营mat2G.py文件，对q进行granger筛选、大小筛选。将关联矩阵，转化成对应的股票节点表格和边表格
7. 进行granger检验，边表格进行更新。
8. 运行plotQ.py，绘制筛选后的q矩阵分布。
9. gephi里根据边的权重进行筛选，剔除弱关联的边
10. 图的属性运算，计算度，modularity class；布局用XX2布局。把度为0的节点都放在外围，度多的节点放在图中间
11. 导出节点和边的属性表格
12. 根据modularity给节点划分社团。



存在一种现象：

少数股票涨停，导致收益率序列后面全是0.

少数股票交易不活跃，导致5分钟内价格没有波动，收益率序列也有很多0.他们的收益率相关性非常高。

涨停股票和涨停股票之间的相关性比较高。



解决方案是收益率计算精度边长。还有就是总的时间边长。

# 时间序列处理的基本过程

[参考文章](https://blog.51cto.com/u_14293657/4220519)

戈兰泽https://www.biaodianfu.com/granger-causality-test.html