#-*- coding: utf-8 -*-

import  numpy as np
import  pandas as pd
import  matplotlib.pyplot as plt
from pandas import  Series,DataFrame
import time
import datetime
from GM11 import GM11
pd.set_option('display.width',None)
inputfile='../data/beijing.xls'
outputfile='../temp/air_data.csv'

data=pd.read_excel(inputfile)
data.to_csv(outputfile,index=False)

data=pd.read_csv(outputfile)

#數據清洗
data=data.dropna(axis=0,how='all')
data=data.drop_duplicates(subset = None, keep = 'first')
data=data.drop(['当天AQI排名'],axis=1)
data=data.drop(['质量等级'],axis=1)
# for i in range(len(data[u'日期'])):
#     data[u'日期'][i]=''.join(data[u'日期'][i].split('-'))
data=data.to_csv('../temp/air_quary.csv',index=False)

print(u'清洗后的数据：')
data=pd.read_csv('../temp/air_quary.csv')
print(data)

#计算相关系数
np.round(data.corr(method='pearson'),2)
print(u'相关系数：')
print(np.round(data.corr(method='pearson'),2))

#计算特征系数(线性回归模型)
from sklearn.linear_model import LinearRegression
model=LinearRegression()
model.fit(data.iloc[:,2:8],data['AQI指数'])
model.coef_
print(model.coef_)

#灰色预测
inputfile ='../temp/air_quary.csv'
outputfile='../temp/air_predict.csv'
modelfile='../tem,/air_predict_net.model'
data=pd.read_csv(inputfile,index_col=u'日期')
print(u'预测时所读取数据：')
print(data)
#
data.loc['2018-09-01'] = None
data.loc['2018-09-02'] = None
print(len(data.index))
# print(data[data.index.duplicated()])
l=['AQI指数','PM2.5','PM10','So2','No2','Co','O3']
for i in l:
    f=GM11(data[i][data.index[0:483]].as_matrix())[0]
    print(f(len(data)-1))
    print(f(len(data)))
    data[i]['2018-09-01']=f(len(data)-1)
    data[i]['2018-09-02']=f(len(data))
    data[i]=data[i].round(2)
print("data:", data)
data.to_csv(outputfile)
import pandas as pd
inputfile = '../temp/air_predict.csv' #灰色预测后保存的路径
outputfile = '../data/revenue.csv' #神经网络预测后保存的结果
modelfile = '../temp/1-net.model' #模型保存路径
data = pd.read_csv(inputfile) #读取数据
data.set_index(u'日期', inplace=True)
feature =['PM2.5','PM10','So2','No2','Co','O3'] #特征所在列
data = data['2017-05-01':'2018-09-02']
data_train = data.copy() #取2014年前的数据建模
print("data_train", type(data_train))
data_mean = data_train.mean()
print("data_mean:", data_mean)
data_std = data_train.std()
print("data_std:", data_std)
data_train = (data_train - data_mean)/data_std #数据标准化
x_train = data_train[feature].as_matrix() #特征数据
y_train = data_train[u'AQI指数'].as_matrix() #标签数据

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
data[u'y_pred'] = model.predict(x) * data_std[u'AQI指数'] + data_mean[u'AQI指数']
data.to_csv(outputfile)

import matplotlib.pyplot as plt #画出预测结果图
p = data[[u'AQI指数','y_pred']].plot(subplots = True, style=['b-o','r-*'])
plt.show()