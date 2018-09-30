# -*- coding: utf-8 -*-
import pandas as pd
import pymysql
import schedule
import time
import datetime
from xpinyin import Pinyin
def airDataToCsv():
    conn = pymysql.connect(host='127.0.0.1', \
                   user='root',password='123.com', \
                   db='testdata',charset='utf8', \
                   use_unicode=True)
    placeItemsFile = '../data/placeItems.csv' #输入的数据文件
    # 查询出所有的监测空气的地区
    placeSql = "SELECT DISTINCT(monitoring_point) from air_quality"
    placeItems = pd.read_sql(placeSql, con=conn)
    #文件名用拼音
    p = Pinyin()
    # 存储监测空气的地区
    placeItems.to_csv(placeItemsFile)
    print("Time:", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))#现在
    for indexs in placeItems.index:
        placeItem= placeItems.loc[indexs].values[0]
        # 去掉空值
        if(placeItem != None):
            airSql = "SELECT DISTINCT air.times,A.target 'SO2',B.target 'NO2',K.target 'O3',D.target 'PM10',E.target 'PM2.5',F.target 'CO',G.target 'AQI' from air_quality air " \
                     " INNER JOIN "\
                     "(select id,times,target  from air_quality  where type_air='1' and monitoring_point ='"+placeItem+"') A "\
                     " on air.times=A.times "\
                     " INNER JOIN "\
                     "(select id,times,target  from air_quality  where type_air='2' and monitoring_point ='"+placeItem+"') B "\
                     " on air.times=B.times "\
                     " INNER JOIN "\
                     "(select id,times,target  from air_quality  where type_air='3' and monitoring_point ='"+placeItem+"') K "\
                     " on air.times=K.times "\
                     " INNER JOIN "\
                     "(select id,times,target  from air_quality  where type_air='4' and monitoring_point ='"+placeItem+"') D "\
                     " on air.times=D.times "\
                     " INNER JOIN "\
                     "(select id,times,target  from air_quality  where type_air='5' and monitoring_point ='"+placeItem+"') E "\
                     " on air.times=E.times "\
                     " INNER JOIN "\
                     "(select id,times,target  from air_quality  where type_air='7' and monitoring_point ='"+placeItem+"') F "\
                     " on air.times=F.times "\
                     " INNER join "\
                     "(select id,times,target  from air_quality where type_air='6' and monitoring_point ='"+placeItem+"') G "\
                     " on air.times=G.times "\
                     " WHERE air.monitoring_point ='"+placeItem+"' order by air.times asc"
            # 预处理表air_quality
            placeItem = p.get_pinyin(placeItem, '')
            AQIData = pd.read_sql(airSql, con=conn)
            placeAir = "../data/"+placeItem + ".csv"
            AQIData.to_csv(placeAir,index=False)
            print("placeAir to csv finished")



schedule.every(2).minutes.do(airDataToCsv)
#schedule.every().hour.do(airDataToCsv)
#schedule.every().day.at("10:30").do(airDataToCsv)
#schedule.every(5).to(10).days.do(airDataToCsv)
#schedule.every().monday.do(airDataToCsv)
#schedule.every().wednesday.at("13:15").do(airDataToCsv)

while True:
    schedule.run_pending()
    time.sleep(1)



