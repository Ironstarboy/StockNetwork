create schema stockData;

drop table stockprice;
create table stockprice(
	Stkcd int,
    Trddt varchar(10),
    Opnprc float,
    Clsprc float,
    Dretnd double,
    Markettype TINYINT,
    Trdsta tinyint,
    PreClosePrice float,
    primary key (Stkcd,Trddt)
);

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


