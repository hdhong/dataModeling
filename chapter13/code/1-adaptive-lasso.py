#-*- coding: utf-8 -*-


import pandas as pd
inputfile = '../data/data1.csv' #输入的数据文件
data = pd.read_csv(inputfile) #读取数据
from sklearn import linear_model
model = linear_model.Lasso(alpha=100)
model.fit(data.iloc[:,0:13],data['y'])
model.coef_  #各个特征的系数
model.intercept_
print("model.coef_:", model.coef_)
print("model.intercept_:", model.intercept_)

# correlation

import numpy as np
import pandas as pd
inputfile = '../data/data1.csv' #输入的数据文件
data = pd.read_csv(inputfile)  #读取数据
np.round(data.corr(method='pearson'), 2) #计算相关系数矩阵，保留两位小数
print("np.round(data.corr(method='pearson'), 2):", np.round(data.corr(method='pearson'), 2))

#gaikuo

import numpy as np
import pandas as pd
inputfile = '../data/data1.csv' #输入的数据文件
data = pd.read_csv(inputfile)  #读取数据
r = [data.min(), data.max(), data.mean(), data.std()] #依次计算最小值、最大值、均值、标准差
r = pd.DataFrame(r,index=['Min', 'Max', 'Mean', 'STD']).T #计算相关系数矩阵
np.round(r, 2) #保留两位小数
print("np.round(r, 2):", np.round(r, 2))

#huise
import numpy as np
import pandas as pd
from  GM11 import GM11

inputfile = '../data/data1.csv' #输入的数据文件
outputfile = '../tmp/data1_GM11.xls' #灰色预测后保存的路径
data = pd.read_csv(inputfile) #读取数据
data.index = range(1994, 2014)

data.loc[2014] = None
data.loc[2015] = None
l = ['x1', 'x2', 'x3', 'x4', 'x5', 'x7']
for i in l:
    f = GM11(data[i].loc[range(1994,2014)].as_matrix())[0]
    print("f:", f)
    data[i][2014] = f(len(data)-1) #2014年预测结果
    data[i][2015] = f(len(data)) #2015年预测结果
    data[i] = data[i].round(2) #保留两位小数

data[l+['y']].to_excel(outputfile) #结果输出
print("data:", data[l+['y']])

#yuce
import pandas as pd
inputfile = '../tmp/data1_GM11.xls' #灰色预测后保存的路径
outputfile = '../data/revenue.xls' #神经网络预测后保存的结果
modelfile = '../tmp/1-net.model' #模型保存路径
data = pd.read_excel(inputfile) #读取数据
feature = ['x1', 'x2', 'x3', 'x4', 'x5', 'x7'] #特征所在列

data_train = data.loc[range(1994,2014)].copy() #取2014年前的数据建模
data_mean = data_train.mean()
data_std = data_train.std()
data_train = (data_train - data_mean)/data_std #数据标准化
x_train = data_train[feature].as_matrix #特征数据
print("x_train", x_train)
y_train = data_train['y'].as_matrix() #标签数据
print("y_train", y_train)
from keras.models import Sequential
from  keras.layers.core import Dense, Dropout, Activation

data_train = data.loc[range(1994,2014)].copy() #取2014年前的数据建模
data_mean = data_train.mean()
data_std = data_train.std()
data_train = (data_train - data_mean)/data_std #数据标准化
x_train = data_train[feature].as_matrix() #特征数据
y_train = data_train['y'].as_matrix() #标签数据

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
data[u'y_pred'] = model.predict(x) * data_std['y'] + data_mean['y']
data.to_excel(outputfile)

import matplotlib.pyplot as plt #画出预测结果图
p = data[['y','y_pred']].plot(subplots = True, style=['b-o','r-*'])
plt.show()