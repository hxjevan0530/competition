# -*- coding: utf-8 -*-
import math
import random
import worstFit
import BP
#import Elman

flavType = 15

random.seed(0)

def make_matrix(m, n, fill=0.0):
    mat = []
    for i in range(m):
        mat.append([fill] * n)
    return mat

def get_median(data):
    data.sort()
    half = len(data) // 2
    return (data[half] + data[~half]) / 2

def get_median_filtered(signal, threshold=3):
    difference = [0] * len(signal)
    for i in range(len(signal)):
        difference[i] = abs(signal[i] - get_median(signal))
    median_difference = get_median(difference)
    if median_difference == 0:
        s = 0
    else:
        for i in range(len(difference)):
            s = difference[i] / median_difference
            if(s>threshold):
                signal[s] = get_median(signal)
    return signal


def festival(tlist):
    List=[[2015,1,1],[2015,1,2],[2015,1,3],[2015,2,18],[2015,2,19],[2015,2,20],[2015,2,21],\
          [2015,2,22],[2015,2,23],[2015,2,24],[2015,4,5],[2015,4,6],[2015,5,1],[2015,5,2],\
          [2015,5,3],[2015,6,20],[2015,6,21],[2015,6,22],[2015,9,26],[2015,9,27],[2015,10,1],\
          [2015,10,2],[2015,10,3],[2015,10,4],[2015,10,5],[2015,10,6],[2015,10,7],[2016,1,1],\
          [2016,1,2],[2016,1,3],[2016,2,7],[2016,2,8],[2016,2,9],[2016,2,10],[2016,2,11],[2016,2,12],\
          [2016,2,13],[2016,4,4],[2016,4,5],[2016,4,6],[2016,5,1],[2016,5,2],\
          [2016,5,3],[2016,6,9],[2016,6,10],[2016,6,11],[2016,9,15],[2016,9,16],[2016,9,17],\
          [2016,10,1],[2016,10,2],[2016,10,3],[2016,10,4],[2016,10,5],[2016,10,6],[2016,10,7],
          [2017,1,1],[2017,1,2],[2017,1,3],[2017,1,27],[2017,1,28],[2017,1,29],[2017,1,30],\
          [2017,2,1],[2017,2,2],[2017,4,2],[2017,4,4],[2017,5,1],[2017,5,2],[2017,5,3],[2017,5,4],\
          [2017,5,5],[2017,5,6],[2017,5,7],[2017,5,28],[2017,5,29],[2017,5,30],[2017,10,1],[2017,10,2],\
          [2017,10,3],[2017,10,4],[2017,10,5],[2017,10,6],[2017,10,7],[2017,10,8],[2015,11,11],[2016,11,11],\
          [2017,11,11],[2018,1,1],[2017,12,30],[2017,12,31],[2018,2,15],[2018,2,16],[2018,2,17],[2018,2,18],\
          [2018,2,19],[2018,2,20],[2018,2,21]]
    for i in range(len(List)):
        if(tlist==List[i]):
            return 1

#将日期转换为星期
weekDay=[[2015,1,1,4],[2015,2,1,7],[2015,3,1,7], [2015,4,1,3],\
         [2015,5,1,5],[2015,6,1,1], [2015,7,1,3], [2015,8,1,6],\
         [2015,9,1,2],[2015,10,1,4],[2015,11,1,7],[2015,12,1,2],\
         [2016,1,1,5],[2016,2,1,1], [2016,3,1,2], [2016,4,1,5],\
         [2016,5,1,7],[2016,6,1,3], [2016,7,1,5], [2016,8,1,1],\
         [2016,9,1,4],[2016,10,1,6],[2016,11,1,2],[2016,12,1,4],\
         [2017,1,1,7],[2017,2,1,3], [2017,3,1,3], [2017,4,1,6],\
         [2017,5,1,1],[2017,6,1,4], [2017,7,1,6], [2017,8,1,2],\
         [2017,9,1,5],[2017,10,1,7],[2017,11,1,3],[2017,12,1,5],\
         [2018,1,1,1],[2018,2,1,4], [2018,3,1,4], [2018,4,1,7]]

def getweekDay(tList):
    week = 0
    for i in range(len(weekDay)):
        if(weekDay[i][0:2]==tList[0:2]):
            week=(tList[2]-weekDay[i][2])%7+weekDay[i][3]
            if(week>7):
                temp=week//7
                week=week-7*temp
            break
    return week

def tranWeek(tList):
    nList = []
    for i in range(len(tList)):
        tempValue=getweekDay(tList[i])
        if(len(bin(tempValue))==3): 
            nList.append([0,0,int(bin(tempValue)[-1])])
        if(len(bin(tempValue))==4): 
            nList.append([0,int(bin(tempValue)[2]),int(bin(tempValue)[3])])
        if(len(bin(tempValue))==5): 
            nList.append([int(bin(tempValue)[2]),int(bin(tempValue)[3]),\
                                                 int(bin(tempValue)[4])])
    return nList
      
#将列表元素进行对数处理，log10
def log10(tList):
    nList = make_matrix(len(tList), len(tList[0]))
    for i in range(len(tList)):
            for j in range(len(tList[0])):
                if(tList[i][j]!=0):
                    nList[i][j] = math.log10(tList[i][j])  
    for i in range(len(nList)):
        for j in range(len(nList[0])):
            if(nList[i][j]>=1):
                nList[i][j]=0
    return nList

def guiyihua(tList):
    nList = [0] * len(tList)
    for i in range(len(tList)):
        if(tList[i] != 0):
                nList[i] = math.log(tList[i], 30)
    return nList

#####################################################################   
def predict_vm(ecs_lines, input_lines):
    
    result = []
    if ecs_lines is None:
        print 'ecs information is none'
        return result
    if input_lines is None:
        print 'input file information is none'
        return result
    
    #####################################################################
    #读取训练数据
    listID   = []
    listYMD  = []
    trainX_0 = []
    trainY_0 = []
    tList_1 = []
    tList_2 = [0] * flavType
    
    for item in ecs_lines:
        values_0 = item.split(" ")
        values = values_0[0].split('\t')
        #存放虚拟机编号，日期 
        listID.append(values[1][6::])
        listYMD.append(values[2])
        
    #整理训练数据，同一天数据存放到一起，得到trainX与trainY
    for i in range(len(listID)):
        if(int(listID[i]) > flavType):
            continue
        tList_2[int(listID[i])-1] += 1
        if(i < len(listID)-1 and listYMD[i] == listYMD[i+1]):
            pass
        else:
            tList_1 = [int(listYMD[i][0:4]), int(listYMD[i][5:7]),\
                     int(listYMD[i][8::])]
            #忽略节假日
            #if(festival(tempList)==1):
                #continue
            trainX_0.append(tList_1)
            trainY_0.append(tList_2)
            tList_1 = []
            tList_2 = [0] * flavType
    
    #打印trainData.txt文件中的信息
    print('trainDataFile:')
    for i in range(len(trainX_0)):
        print(trainX_0[i], trainY_0[i])
        
    #####################################################################
    #读取输入数据
    vmID          = []
    vmCore        = []
    vmMem         = []
    FEdate        = []
    testX_0       = []
    considerRe    = 0
    pCoreNumber   = 0
    pMemoryNumber = 0
    
    for item in input_lines:
        value_0 = item.split('\n')
        value_1 = value_0[0].split('\r')
        value_2 = value_1[0]
        value   = value_2.split(' ')
        #根据输入数据长短判断类型
        if(len(value) == 3):
            if(len(value[0]) > 6):
                vmID.append(int(value[0][6::]))
                vmCore.append(int(value[1]))
                vmMem.append(int(value[2]))
                continue
            else:
                pCoreNumber   = int(value[0])
                pMemoryNumber = int(value[1]) * 1024
                continue
        elif(len(value) == 2):
            FEdate.append(value[0])
            continue
        elif(len(value) == 1):
            if(value[0] == 'CPU'):
                considerRe = 1
                continue
            elif(value[0] == 'MEM'):
                considerRe = 0
                continue

    #打印input.txt文件中的信息
    print('inputFile:')
    
    #虚拟机种类
    vmType = len(vmID)
    
    #物理机CPU核心数及内存大小
    print('pCoreNumber:',pCoreNumber,'pMemoryNumber:',pMemoryNumber)
    
     #虚拟机类型，CPU核心数及内存大小
    print('VMType:',vmType,'VMID:',vmID,'VMcore:',vmCore,'VMmem:',vmMem)
    
    #优先考虑资源  CPU为1  MEM为0
    print('firstRe:',considerRe)
    
    #预测时间范围
    print('firstDate:',FEdate[0],'endDate:',FEdate[1])
    
    #根据开始结束日期确定时间范围
    tempY = int(FEdate[0][0:4])
    tempM = int(FEdate[0][5:7])
    tempD = int(FEdate[0][8::])
    while(tempY != int(FEdate[1][0:4]) or tempM != int(FEdate[1][5:7])\
                                       or tempD != int(FEdate[1][8::])):  
        if((tempD>30 and tempM==4) or (tempD>30 and tempM==6) or \
           (tempD>30 and tempM==9) or (tempD>30 and tempM==11) or \
           (tempD>31 and tempM==1) or (tempD>31 and tempM==3) or \
           (tempD>31 and tempM==5) or (tempD>31 and tempM==7) or \
           (tempD>31 and tempM==8) or (tempD>31 and tempM==10) or \
           (tempD>31 and tempM==12)or (tempD>28 and tempM==2)):
            tempD =  1
            tempM += 1
        if(tempM>12):
            tempM =  1
            tempY += 1
        testX_0.append([tempY, tempM, tempD])
        tempD += 1
        
    print(testX_0)
    
    #####################################################################
    #trainX_0 --- 训练数据日期;
    #trainY_0 --- 每天虚拟机需求;
    #testX_0  --- 待求日期虚拟机需求.

    trainx_1 = []
    trainy_1 = []
    testx_1  = []
    testy    = []

    trainx_2 = []
    trainy_2 = []
    testx_2  = []
    #检验模型
    #trainx=[[0.9413,0.4707,0.6953,0.8133,0.9379,0.4677,0.6981,0.8002,0.9517,0.4725,0.7006,0.8201],\
        #[0.9379,0.4677 ,0.6981, 0.8002 ,0.9517 ,0.4725, 0.7006, 0.8201 ,0.9557, 0.4790, 0.7019 ,0.8211],\
        #[0.9517, 0.4725, 0.7006 ,0.8201, 0.9557 ,0.4790 ,0.7019 ,0.8211 ,0.9601 ,0.4811, 0.7101, 0.8298]]
    #trainy=[[0.9557 ,0.4790 ,0.719 ,0.8211],[0.9601 ,0.4811 ,0.7101 ,0.8298], [0.9612 ,0.4845 ,0.7188 ,0.8312]]
    #trainx_1=trainx
    #trainx_2=trainx
    #trainy_1=trainy
    #trainy_2=trainy
    
    #处理异常点,将大于15的数据置0
    #for i in range(len(trainY_0)):
        #for j in range(len(trainY_0[0])):
            #if(trainY_0[i][j] >= 15):
                #trainY_0[i][j] = 0
     
    trainx_1 = tranWeek(trainX_0)
    trainx_2 = trainx_1
        
    trainy_2 = trainY_0
    testx_1  = tranWeek(testX_0)
    testx_2  = testx_1  
    print trainx_2
    print trainy_2
    print testx_2

    testy    = [0,13,3,0,2,0,2,6,15,2,5,1,0,7,2]#2015.2.20-2015.2.26真实值
    testy_1 = [0, 0, 1, 0, 0, 0, 1, 2, 1, 0, 4, 1, 0, 7, 2]
    testy_2 = [0, 0, 1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0]
    testy_3 = [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    testy_4 = [0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 1, 0, 0, 0, 0]
    #####################################################################
    #预测虚拟机需求
    predictList = [0] * flavType

    #训练过程
    #RNN
    #rnn = Elman.RNN()
    #rnn.setup(len(trainx_1[0]), 20, len(trainy_1[0]), len(trainx_1), 0.09, 0.1)
    #rnn.train(trainx_1, trainy_1, 1000, 1.0e-04)

    #BP
    bp=BP.BPNetwork()
    bp.setup(len(trainx_2[0]),20,len(trainy_2[0]))
    bp.train(trainx_2,trainy_2,500,0.09,0.1)

    tList = []
    for i in range(len(testx_2)):
        tList = bp.predict(testx_2[i])
        for j in range(len(tList)):
            tList[j] = int(round(tList[j]))
            if tList[j] < 0:
                tList[j] = 0
        print tList
        for j in range(flavType):
            predictList[j] += tList[j]
        tList = []  
    
    print('testy ', testy)
    print('pdicty', predictList) 
    Error = 0
    for i in range(len(testy)):
        Error += abs(testy[i]-predictList[i])
    print('predict error:', Error)
    
    '''
    #####################################################################
    #将预测虚拟机需求信息写入文件
    sumVMNum = 0
    
    #预测虚拟机总数量
    for i in range(len(vmID)):
        sumVMNum += predictList[vmID[i]-1]
    result.append(str(int(sumVMNum)))
    
    #每种虚拟机数量
    for i in range(len(vmID)):
        result.append('flavor'+str(int(vmID[i]))+' '+\
                      str(int(predictList[vmID[i]-1])))
    result.append('\n')
    
    #####################################################################
    #worst_fit方法装箱
    flag_1   = 0
    result_1 = []
    pNum     = []
    [flag_1, result_1, pNum] = worstFit.dist(pCoreNumber, pMemoryNumber,\
                    vmType, predictList, vmID, vmMem, vmCore, considerRe)
        
    #####################################################################
    #将结果信息写入文件
    while(flag_1 < len(result_1)):
        if(flag_1 < len(result_1)-1 and \
        result_1[flag_1][0] == result_1[flag_1+1][0]):
            result_1[flag_1].extend([result_1[flag_1+1][1],\
                                 int(result_1[flag_1+1][2])])
            del result_1[flag_1+1]
        else:
            flag_1 += 1
            
    result.append(str(pNum))
    
    for i in range(len(result_1)):
        for j in range(len(result_1[i])):
            if(j == 0):
                string = str(result_1[i][j])
            else:
                string += ' '+str(result_1[i][j])
        
        result.append(string)
    
    #####################################################################
    '''
    return result


array_1 = []
with open('trainData.txt', 'r') as lines:
    for line in lines:
        array_1.append(line)
array_2 = []
with open('input.txt', 'r') as lines:
    for line in lines:
        array_2.append(line)

res=predict_vm(array_1,array_2)
print(res)

