# -*- coding: cp1251 -*-
from csvkit.utilities.csvsql import CSVSQL

args_query = ['--query','select APPLICATION_DT as Date, INTERNAL_ORG_ORIGINAL_RK as Pos,LOAN_AMOUNT as \'Сумма выдач\'  from data','data.csv']
result  = CSVSQL(args_query)
print(result.main())