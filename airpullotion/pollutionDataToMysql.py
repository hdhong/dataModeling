#-*- coding: utf-8 -*-
import pymysql
from datetime import datetime
from pandas import read_csv
#sheet = book.sheet_by_name("@beijing")
#建立一个MySQL连接
conn = pymysql.connect(
        host='127.0.0.1',
        user='root',
        passwd='123.com',
        db='testdata',
        port=3306,
        charset='utf8'
        )
# 获得游标
cur = conn.cursor()
data = read_csv("pollution.csv", header=0, index_col=0)
# 创建插入SQL语句
for indexs in data.index:
    date = indexs
    pollution = float(data.loc[indexs].values[0:1])
    dew = float(data.loc[indexs].values[1:2])
    temp = float(data.loc[indexs].values[2:3])
    press = float(data.loc[indexs].values[3:4])
    wnd_dir = str(data.loc[indexs].values[4:5][0])
    wnd_spd = float(data.loc[indexs].values[5:6])
    snow = float(data.loc[indexs].values[6:7])
    rain = float(data.loc[indexs].values[7:8])
    values = (date, pollution, dew, temp, press, wnd_dir, wnd_spd, snow, rain)
    sql = 'insert into pollution (date,pollution,dew,temp,press,wnd_dir,wnd_spd,snow,rain) values (%s, %s, %s,%s, %s, %s, %s, %s, %s)'
    # 执行sql语句
    cur.execute(sql, values)
conn.commit()
cur.close()
conn.close()
print("data.describe()", data.describe())

