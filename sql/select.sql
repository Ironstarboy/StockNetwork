
show variables like 'SQL_SAFE_UPDATES';
SET SQL_SAFE_UPDATES = 0;
delete from stockprice where Trddt in ('Trddt', '交易日期' ,'没有单位');
delete FROM stockprice WHERE Stkcd =  NULL;

select * FROM stockprice ;


alter table stockprice add lnReturn float;


select * from stockprice order by Stkcd,Trddt asc;

 update stockprice 
 set lnReturn=log(Clsprc)-log(Opnprc);

UPDATE stockprice 
   SET Trddt = str_to_date(Trddt, '%Y-%m-%d');
   
select distinct Stkcd from stockprice  order by Stkcd desc;
   
select stkcd,count(lnReturn) as num from stockprice group by Stkcd order by num asc;

select distinct trdsta from stockprice ;


select stkcd,count(*) n from stockprice 
group by stkcd 
having count(Trdsta=1)>100 
order by n desc;

select * from stockprice where stkcd=585;


select * from stockprice where stkcd=301268 ;


select s1.lnreturn,s2.lnreturn ,s1.trddt,s2.trddt
from stockprice s1,stockprice s2
where s1.trddt=s2.trddt
and s1.stkcd=1
and s2.stkcd=301268;

select s1.lnreturn,s2.lnreturn ,s1.trddt,s2.trddt
from stockprice s1,stockprice s2
where s1.trddt=s2.trddt
and s1.stkcd=301268
and s2.stkcd=1;

select distinct Stkcd from stockprice where  Markettype=64;

select * from stockprice where stkcd in (430047);





       
       


