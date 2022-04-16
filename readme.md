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