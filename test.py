# -*- coding: UTF-8 -*-
'''
Created on 2015年6月6日

@author: lisongwei
'''
import json

from cx_Oracle import Cursor
import cx_Oracle
import django
from django.contrib.auth.models import User

from SPM.models import TabBdataCommonOrg, CustomUser, TabBdataFacSpeciality, \
    TabBdataFacSpInfo, TabBdataFacCategory
import datetime
db = cx_Oracle.connect('thunder','thunder','192.168.1.101:1521/ORCL')
cursor = db.cursor()

django.setup()

#测试调用oraclefunction
SQL = """select generate_key(5) from dual"""
SQL2 = """select generate_key(32) from dual"""
cursor.execute(SQL) 
result = cursor.fetchall()[0][0]
print result
cursor.execute(SQL2) 
result = cursor.fetchall()[0][0]
print result
#测试时间
# fcda = "2015/05/14"
# fcti = "13:00:34"
# ca = fcda+" "+fcti
ss = u"%s %s"%("ni","wo")
facindate = "06/12/2015"
facintime = "14:19:41"
facindatetimestr = u"%s %s"%(facindate,facintime)
print facindatetimestr
facindatetime = datetime.datetime.strptime(facindatetimestr,'%m/%d/%Y %H:%M:%S')
print facindatetime
# sa = datetime.datetime.strptime(ca,'%Y/%m/%d %H:%M:%S')
# print ca
# print sa
# sss = [1,2,3,4,5]
# for s in sss:
#     print sss.index(s)+1