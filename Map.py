import numpy as np
import pandas as pd

def makeClf():
    #nrows：文件读取的函数（从文件头算起）
    #训练数据x,第一天三时，所有坐标
    trainX_1=pd.read_csv('trainDataX.csv',nrows=2307080)
    #训练数据y,第一天三时，所有坐标
    trainY_1=pd.read_csv('trainDataY.csv',nrows=230708)
    trainX_2=trainX_1.values#获得训练数据x数组
    trainX_3=trainX_2[:,5]#取第六列风速
    trainX=trainX_3.reshape((230708,10))#转换矩阵形式
    trainY_2=trainY_1.values#获得训练数据y数组
    trainY=trainY_2[:,4]#取第五列风速
    return trainX, trainY



def makeMap(h,dateID,clf):
    m=2307080*(h-3+18*(dateID-6))
    #测试数据x,第六天三时,所有坐标
    testX_1=pd.read_csv('testDataX.csv',skiprows=m, nrows=2307080)
    testX_2=testX_1.values#获得测试数据x数组
    testX_3=testX_2[:,5]#取第六列风速
    testX=testX_3.reshape((230708,10))#转换矩阵形式    
    #测试数据进行测试
    testY_1=clf.predict(testX)# 预测结果230708*1列
    testY_2=testY_1.reshape((548,421))
    testY=np.zeros((548,421))
    #将预测数据转换成0，1矩阵（548×421）
    for i in range(548):
        for j in range(421):
            if testY_2[i,j]>=15.0:
                testY[i,j]=1.0
                   
    return testY,testY_2

    
