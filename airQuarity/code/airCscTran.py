#-*- coding: utf-8 -*-
from __future__ import print_function
import pandas as pd
#初始化参数
dish_profit = '../data/air.csv'
inputfile = '../data/AQI.csv' #输入的数据文件
inputfile = '../data/AQI2.csv' #输入的数据文件
data = pd.read_csv(dish_profit, encoding = 'utf8')
#print("data:", data)
xdata = data[['monitoring_point','target','times','type_air']].copy()
monitoring_point = xdata[xdata.monitoring_point == '万顷沙']
monitoring_point.to_csv(inputfile)
print("monitoring_point:", monitoring_point)
#monitoring_point.set_index(["monitoring_point"], inplace=True)


