# -*- coding: cp1251 -*-
from csvkit.utilities.csvsql import CSVSQL

s = u'Сумма выдач'
column_name_summa = s.encode('cp1251')
column_name_summa = column_name_summa.decode('utf8')
args_query = ['--query',"""

select  d1.APPLICATION_DT, 0, 0 from data as d1

group by d1.INTERNAL_ORG_ORIGINAL_RK
order by d1.INTERNAL_ORG_ORIGINAL_RK
;

create temp table t1 (
    ACCOUNT_RK,
    INTERNAL_ORG_ORIGINAL_RK,
    LOAN_AMOUNT,
    APPLICATION_DT
)
;

insert into t1 (ACCOUNT_RK,INTERNAL_ORG_ORIGINAL_RK,LOAN_AMOUNT,APPLICATION_DT)
select  0, 0, 0, d1.APPLICATION_DT from data as d1
group by d1.APPLICATION_DT
order by d1.APPLICATION_DT
;

create temp table t2 (
    ACCOUNT_RK,
    INTERNAL_ORG_ORIGINAL_RK,
    LOAN_AMOUNT,
    APPLICATION_DT
)
;

insert into t2 (ACCOUNT_RK,INTERNAL_ORG_ORIGINAL_RK,LOAN_AMOUNT,APPLICATION_DT)
select  0, data2.INTERNAL_ORG_ORIGINAL_RK,  data2.LOAN_AMOUNT, data1.APPLICATION_DT from t1 as data1
left join (select ACCOUNT_RK, INTERNAL_ORG_ORIGINAL_RK,LOAN_AMOUNT,APPLICATION_DT from data) as data2 on (data1.APPLICATION_DT = data2.APPLICATION_DT)
;



create temp table t3 (
    ACCOUNT_RK,
    INTERNAL_ORG_ORIGINAL_RK,
    LOAN_AMOUNT,
    APPLICATION_DT 
);

insert into t3 (ACCOUNT_RK,INTERNAL_ORG_ORIGINAL_RK,LOAN_AMOUNT,APPLICATION_DT)
select 0,data.INTERNAL_ORG_ORIGINAL_RK, 0, 0 from data
group by INTERNAL_ORG_ORIGINAL_RK;

create temp table t4 (
    ACCOUNT_RK,
    INTERNAL_ORG_ORIGINAL_RK,
    LOAN_AMOUNT,
    APPLICATION_DT 
);

insert  into t4 (ACCOUNT_RK,INTERNAL_ORG_ORIGINAL_RK,LOAN_AMOUNT,APPLICATION_DT)
select 0, INTERNAL_ORG_ORIGINAL_RK, LOAN_AMOUNT, APPLICATION_DT  from t2 group by APPLICATION_DT,INTERNAL_ORG_ORIGINAL_RK  order by APPLICATION_DT  
;

create temp table t5 (
    ACCOUNT_RK,
    INTERNAL_ORG_ORIGINAL_RK,
    LOAN_AMOUNT,
    APPLICATION_DT 
);

insert into t5 (ACCOUNT_RK, APPLICATION_DT, INTERNAL_ORG_ORIGINAL_RK,LOAN_AMOUNT)
select 0, APPLICATION_DT as Date, CAST(INTERNAL_ORG_ORIGINAL_RK as INT) as Pos, sum(LOAN_AMOUNT)   from t2
group by APPLICATION_DT, INTERNAL_ORG_ORIGINAL_RK  order by APPLICATION_DT, INTERNAL_ORG_ORIGINAL_RK;
;

create temp table t6 (
    ACCOUNT_RK,
    INTERNAL_ORG_ORIGINAL_RK,
    LOAN_AMOUNT,
    APPLICATION_DT 
);

insert into t6 (ACCOUNT_RK, APPLICATION_DT, INTERNAL_ORG_ORIGINAL_RK,LOAN_AMOUNT)
select 0, data2.APPLICATION_DT, CAST(data1.INTERNAL_ORG_ORIGINAL_RK as INT),  data5.summa as LOAN_AMOUNT from t3 as data1
left join (select APPLICATION_DT,INTERNAL_ORG_ORIGINAL_RK,  t2.* from   t2 ) as data2
on data1.INTERNAL_ORG_ORIGINAL_RK = data1.INTERNAL_ORG_ORIGINAL_RK
inner join (select t5.APPLICATION_DT, t5.INTERNAL_ORG_ORIGINAL_RK, t5.LOAN_AMOUNT as summa, t5.* from t5 as t5) as data5
on (data5.INTERNAL_ORG_ORIGINAL_RK = data1.INTERNAL_ORG_ORIGINAL_RK) and (data5.APPLICATION_DT = data2.APPLICATION_DT)
group by data2.APPLICATION_DT, data1.INTERNAL_ORG_ORIGINAL_RK
order by data2.APPLICATION_DT,data2.INTERNAL_ORG_ORIGINAL_RK, data2.INTERNAL_ORG_ORIGINAL_RK
;



select data1.APPLICATION_DT as Date, CAST(data5.INTERNAL_ORG_ORIGINAL_RK as INT) as Pos,
case  when data1.APPLICATION_DT != data5.APPLICATION_DT then 0 else data5.summa
end as '%s'
from (select * from t1) as data1
inner join  (select  t6.LOAN_AMOUNT as summa, t6.* from t6) as data5
on (data5.ACCOUNT_RK = data1.ACCOUNT_RK)
group by  data1.APPLICATION_DT,data5.APPLICATION_DT, data5.INTERNAL_ORG_ORIGINAL_RK
order by  data1.APPLICATION_DT,data5.APPLICATION_DT, data5.INTERNAL_ORG_ORIGINAL_RK
;

""" % column_name_summa,'data.csv']
result  = CSVSQL(args_query)

print(result.main())