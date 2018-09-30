#-*- coding: utf-8 -*-


import pandas as pd
import numpy as np
from  GM11 import GM11

inputfile = '../data/data1.csv' #输入的数据文件
data = pd.read_csv(inputfile) #读取数据
from sklearn import linear_model
model = linear_model.Lasso(alpha=1)
model.fit(data.iloc[:,1:6],data['AQI'])
model.coef_  #各个特征的系数
model.intercept_
print("model.coef_:", model.coef_)
print("model.intercept_:", model.intercept_)

np.round(data.corr(method='pearson'), 2) #计算相关系数矩阵，保留两位小数
print("np.round(data.corr(method='pearson'), 2):", np.round(data.corr(method='pearson'), 2))

outputfile = '../tmp/data1_GM11.xls' #灰色预测后保存的路径
data = pd.read_csv(inputfile) #读取数据
data.loc['2018-09-20 21:00:00'] = None
data.loc['2018-09-20 22:00:00'] = None
l = ['SO2','NO2','O3','PM10','PM2.5','CO','AQI']
for i in l:
    f = GM11(data[i].loc[data['times']].as_matrix())[0]
    print("f:", f)
    data[i]['2018-09-20 21:00:00'] = f(len(data)-1) #2014年预测结果
    data[i]['2018-09-20 22:00:00'] = f(len(data)) #2015年预测结果
    data[i] = data[i].round(2) #保留两位小数

data[l+['y']].to_excel(outputfile) #结果输出
print("data:", data[l+['y']])