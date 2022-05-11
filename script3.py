# -*- coding: cp1251 -*-
from csvkit.utilities.csvsql import CSVSQL

s = u'Сумма выдач'
column_name_summa = s.encode('cp1251')
column_name_summa = column_name_summa.decode('utf8')
args_query = ['--query',"""

select  DISTINCT  data.INTERNAL_ORG_ORIGINAL_RK, data.APPLICATION_DT, sum(pos_tb.LOAN_AMOUNT)
from data  
left join (select APPLICATION_DT, LOAN_AMOUNT, INTERNAL_ORG_ORIGINAL_RK, ACCOUNT_RK from data) as  pos_tb on (data.ACCOUNT_RK = pos_tb.ACCOUNT_RK)  
group by  data.INTERNAL_ORG_ORIGINAL_RK,data.APPLICATION_DT
order by  data.INTERNAL_ORG_ORIGINAL_RK,data.APPLICATION_DT

""" ,'data.csv']
result  = CSVSQL(args_query)
print(result.main())