# -*- coding: utf-8 -*-
import pandas as pd
import pymysql
import xlrd
import schedule
import time
import datetime
from xpinyin import Pinyin

conn = pymysql.connect(host='127.0.0.1', \
               user='root',password='123.com', \
               db='testdata',charset='utf8', \
               use_unicode=True)
filename = '../data/beijing.xls'
#data = pd.read_excel(filename)
# 查询出所有的监测空气的地区

cur = conn.cursor()

sql = 'insert into air_data (date, AQI, AQI_ranking, PM2.5, PM10, So2, No2, Co, O3) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)'

book = xlrd.open_workbook(filename)
sheet = book.sheet_by_name('@sheet1')
for r in range(1, sheet.nrows):
    values = (sheet.cell(r, 0).value, sheet.cell(r, 1).value, sheet.cell(r, 2).value, sheet.cell(r, 3).value)
    print(values)
    #cur.execute(sql, values)
#conn.commit()
cur.close()
conn.close()
