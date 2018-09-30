#-*- coding: utf-8 -*-
import pymysql
import  numpy as np
import  pandas as pd
from xlrd import xldate_as_tuple
import  matplotlib.pyplot as plt
from pandas import  Series,DataFrame
import time
import datetime
from GM11 import GM11
def pridictDataToMysql(data):
    for indexs in data.index:
        date = indexs
        AQI = float(data.loc[indexs].values[0:1])
        PM25 = float(data.loc[indexs].values[1:2])
        PM10 = float(data.loc[indexs].values[2:3])
        So2 = float(data.loc[indexs].values[3:4])
        No2 = float(data.loc[indexs].values[4:5])
        Co = float(data.loc[indexs].values[5:6])
        O3 = float(data.loc[indexs].values[6:7])
        AQI_pred = float(data.loc[indexs].values[7:8])
        sql = 'insert into air_pridict_data (date, AQI, PM25, PM10, So2, No2, Co, O3,AQI_pred) values (%s, %s, %s,%s, %s, %s, %s, %s, %s)'
        values = (date, AQI, PM25, PM10, So2, No2, Co, O3, AQI_pred)
        # 执行sql语句
        cur = conn.cursor()
        cur.execute(sql, values)
        cur.close()

pd.set_option('display.width',None)
#inputfile='../data/beijing.xls'


conn = pymysql.connect(host='127.0.0.1', \
                       user='root', password='123.com', \
                       db='testdata', charset='utf8', \
                       use_unicode=True)
# 查询出所有的监测空气的地区
placeSql = "SELECT date,quality_grade,AQI_ranking,PM25,PM10,So2,No2,Co,O3,AQI  from air_data"
data = pd.read_sql(placeSql, con=conn)
#數據清洗
data=data.dropna(axis=0,how='all')
data=data.drop_duplicates(subset = None, keep = 'first')
data=data.drop(['AQI_ranking'],axis=1)
data=data.drop(['quality_grade'],axis=1)
print(u'清洗后的数据：')
print(data)
#计算相关系数
np.round(data.corr(method='pearson'),2)
print(u'相关系数：')
print(np.round(data.corr(method='pearson'),2))

#计算特征系数(线性回归模型)
from sklearn.linear_model import LinearRegression
model=LinearRegression()
model.fit(data.iloc[:,2:8],data['AQI'])
model.coef_
print(model.coef_)
#inputfile ='../temp/air_quary1.csv'
#data.to_csv(inputfile,index=False)
#data=pd.read_csv(inputfile,index_col=u'date')
data.set_index(u'date', inplace=True)
data.loc['2018-09-01'] = None
data.loc['2018-09-02'] = None
print(len(data.index))
# print(data[data.index.duplicated()])
l=['PM25','PM10','So2','No2','Co','O3','AQI']
for i in l:
    f=GM11(data[i][data.index[0:483]].as_matrix())[0]
    print(f(len(data)-1))
    print(f(len(data)))
    data[i]['2018-09-01']=f(len(data)-1)
    data[i]['2018-09-02']=f(len(data))
    data[i]=data[i].round(2)
print("data11111:", data)
outputfile='../temp/air_predict1.csv'
#data.to_csv(outputfile)
data1 = data
data = data1
import pandas as pd
modelfile = '../temp/1-net.model' #模型保存路径
inputfile='../temp/air_predict1.csv'
pridictfile='../temp/predict.csv'
data = pd.read_csv(inputfile) #读取数据
data.set_index(u'date', inplace=True)
feature =['PM25','PM10','So2','No2','Co','O3'] #特征所在列
data = data['2017-05-01':'2018-09-02']
data_train = data.copy() #取2014年前的数据建模
print("data_train", type(data_train))
data_mean = data_train.mean()
print("data_mean:", data_mean)
data_std = data_train.std()
print("data_std:", data_std)
data_train = (data_train - data_mean)/data_std #数据标准化
x_train = data_train[feature].as_matrix() #特征数据
y_train = data_train[u'AQI'].as_matrix() #标签数据

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation

model = Sequential() #建立模型
model.add(Dense(input_dim=6, output_dim=12))
model.add(Activation('relu')) #用relu函数作为激活函数，能够大幅提供准确度
model.add(Dense(input_dim=12, output_dim=1))
model.compile(loss='mean_squared_error', optimizer='adam') #编译模型
model.fit(x_train, y_train, nb_epoch = 10000, batch_size = 16) #训练模型，学习一万次
model.save_weights(modelfile) #保存模型参数

#预测，并还原结果。
x = ((data[feature] - data_mean[feature])/data_std[feature]).as_matrix()
data[u'AQI_pred'] = model.predict(x) * data_std[u'AQI'] + data_mean[u'AQI']
data.to_csv(pridictfile)
import matplotlib.pyplot as plt #画出预测结果图
p = data[[u'AQI','AQI_pred']].plot(subplots = True, style=['b-o','r-*'])
plt.show()
pridictDataToMysql(data)

conn.commit()
conn.close()

