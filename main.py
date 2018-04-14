import math
import numpy as np
import pandas as pd
import AstarClass
import Map
from sklearn import linear_model

#########################################################
'''
#线性回归拟合函数
[trainX,trainY]=Map.makeClf()
clf=linear_model.LinearRegression()
clf.fit(trainX,trainY)
'''
#########################################################
#寻路
def find_path(x1, y1, x2, y2,tmap,rmap):   
    s_x = y1
    s_y = x1
    e_x = y2
    e_y = x2
    t_tmap= tmap
    t_rmap= rmap

    #实例化一个Astar对象
    a_star = AstarClass.A_Star(s_x, s_y, e_x, e_y, t_tmap, t_rmap)  
    a_star.find_path()
    fpath=[]
    path_0 = a_star.path
    #路径倒置，第一个点为起点，最后一个点为终点
    path_1=path_0[::-1]
    for line in path_1:
        line=list(line)
        fpath.append(line)
        
    if(len(fpath)>30):      
        return fpath, 1
    elif(len(fpath)==0):
        return fpath, 2
    else:
        return fpath, 0
    
#打印起点终点信息
def printSE(tmap,startx,starty,endx,endy):
    print("本次起点为：", startx, starty)
    print("本次终点为：", endx, endy)
    print("起点周围坐标：")
    print(tmap[startx-4:startx+3, starty-4:starty+3])
    print("终点周围坐标：")
    print(tmap[endx-4:endx+3, endy-4:endy+3])
    
#向周围搜索可走的点。输入开始搜索的点，搜索最大距离，搜索方向，搜索的地图
#搜寻成功，返回点坐标，路径
def searchLocation(startx,starty,length,tmap1,tmap2):
    zm=np.zeros((548,421))
    p=1#从里向外搜索
    e=0#搜寻成功标志位
    temppath=[]
    spath=[]
    Spath=[]
    lpath=[]
    while(p<=length and p>0):
        tempx=startx-p
        tempy=starty
        while(tempx!=startx and tempy!=starty-p):
            tempx=tempx+1
            tempy=tempy-1 
            if(tempx<=1 or tempx>=548):
                tempx=tempx-1
            if(tempy<=1 or tempy>=421):
                tempy=tempy+1
            #如果搜寻成功
            if((not(1 in tmap1[tempx-3:tempx+2,tempy-3:tempy+2])) and \
                (not(1 in tmap2[tempx-3:tempx+2,tempy-3:tempy+2]))):
                [temppath, tagC]=find_path(startx,starty,tempx,tempy,tmap1,zm)
                if(tagC!=2):
                    spath.append([tempx,tempy])
                    Spath.append(temppath)
                    lpath.append([len(temppath)-1,p])
                    e=e+1
                    
        while(tempx!=startx+p and tempy!=starty):
            tempx=tempx+1
            tempy=tempy+1
            if(tempx<=1 or tempx>=548):
                tempx=tempy-1
            if(tempy<=1 or tempy>=421):
                tempy=tempy-1
            if((not(1 in tmap1[tempx-3:tempx+2,tempy-3:tempy+2])) and \
                (not(1 in tmap2[tempx-3:tempx+2,tempy-3:tempy+2]))):
                [temppath,tagC]=find_path(startx,starty,tempx,tempy,tmap1,zm)
                if(tagC!=2):
                    spath.append([tempx,tempy])
                    Spath.append(temppath)
                    lpath.append([len(temppath)-1,p])
                    e=e+1
                        
        while(tempx!=startx and tempy!=starty+p):
            tempx=tempx-1
            tempy=tempy+1
            if(tempx<=1 or tempx>=548):
                tempx=tempx+1
            if(tempy<=1 or tempy>=421):
                tempy=tempy-1
            if((not(1 in tmap1[tempx-3:tempx+2,tempy-3:tempy+2]))and\
              (not(1 in tmap2[tempx-3:tempx+2,tempy-3:tempy+2]))):
                [temppath,tagC]=find_path(startx,starty,tempx,tempy,tmap1,zm)
                if(tagC!=2):
                    spath.append([tempx,tempy])
                    Spath.append(temppath)
                    lpath.append([len(temppath)-1,p])
                    e=e+1
                    
        while(tempx!=startx-p and tempy!=starty):
            tempx=tempx-1
            tempy=tempy-1
            if(tempx<=1 or tempx>=548):
                tempx=tempx+1
            if(tempy<=1 or tempy>=421):
                tempy=tempy+1
            if((not(1 in tmap1[tempx-3:tempx+2,tempy-3:tempy+2])) and \
                (not(1 in tmap2[tempx-3:tempx+2,tempy-3:tempy+2]))):
                [temppath,tagC]=find_path(startx,starty,tempx,tempy,tmap1,zm)
                if(tagC!=2):
                    spath.append([tempx,tempy])
                    Spath.append(temppath)
                    lpath.append([len(temppath)-1,p])
                    e=e+1
        p=p+1

    #搜索成功，返回所有合适位置坐标
    o=0
    if(e>0):
        print(lpath[0][0],lpath[0][1])
        wx=spath[0][0]
        wy=spath[0][1]
        wp=Spath[0]
        if(lpath[0][0]>lpath[0][1]):
            for t in range(len(spath)):
                if(spath[0][0]==spath[t][0] and spath[0][1]==spath[t][1] and lpath[t][0]<=lpath[t][1]):
                    wx=spath[t][0]
                    wy=spath[t][1]
                    wp=Spath[t]
                    print(lpath[0][0],lpath[0][1])
                    o=1
                    break
            if(o==0):
                print("搜寻失败",startx,starty,"周围没有合适的位置")
                return [],[],1
        
        return [wx,wy],wp[1::],0
    else:
        print("搜寻失败",startx,starty,"周围没有合适的位置")
        return [],[],1

def searchLocationB(startx,starty,length,tmap1,tmap2):
    zm=np.zeros((548,421))
    p=1#从里向外搜索
    e=0#搜寻成功标志位
    temppath=[]
    spath=[]
    Spath=[]
    lpath=[]
    while(p<=length and p>0):
        tempx=startx-p
        tempy=starty
        while(tempx!=startx and tempy!=starty-p):
            tempx=tempx+1
            tempy=tempy-1 
            if(tempx<=1 or tempx>=548):
                tempx=tempx-1
            if(tempy<=1 or tempy>=421):
                tempy=tempy+1
            #如果搜寻成功
            if((not(1 in tmap1[tempx-3:tempx+2,tempy-3:tempy+2])) and \
               tmap2[tempx-1,tempy-1]==0):
                [temppath, tagC]=find_path(startx,starty,tempx,tempy,tmap1,zm)
                if(tagC!=2):
                    spath.append([tempx,tempy])
                    Spath.append(temppath)
                    lpath.append([len(temppath)-1,p])
                    e=e+1
                    
        while(tempx!=startx+p and tempy!=starty):
            tempx=tempx+1
            tempy=tempy+1
            if(tempx<=1 or tempx>=548):
                tempx=tempy-1
            if(tempy<=1 or tempy>=421):
                tempy=tempy-1
            if((not(1 in tmap1[tempx-3:tempx+2,tempy-3:tempy+2])) and \
               tmap2[tempx-1,tempy-1]==0):
                [temppath,tagC]=find_path(startx,starty,tempx,tempy,tmap1,zm)
                if(tagC!=2):
                    spath.append([tempx,tempy])
                    Spath.append(temppath)
                    lpath.append([len(temppath)-1,p])
                    e=e+1
                        
        while(tempx!=startx and tempy!=starty+p):
            tempx=tempx-1
            tempy=tempy+1
            if(tempx<=1 or tempx>=548):
                tempx=tempx+1
            if(tempy<=1 or tempy>=421):
                tempy=tempy-1
            if((not(1 in tmap1[tempx-3:tempx+2,tempy-3:tempy+2])) and \
               tmap2[tempx-1,tempy-1]==0):
                [temppath,tagC]=find_path(startx,starty,tempx,tempy,tmap1,zm)
                if(tagC!=2):
                    spath.append([tempx,tempy])
                    Spath.append(temppath)
                    lpath.append([len(temppath)-1,p])
                    e=e+1
                    
        while(tempx!=startx-p and tempy!=starty):
            tempx=tempx-1
            tempy=tempy-1
            if(tempx<=1 or tempx>=548):
                tempx=tempx+1
            if(tempy<=1 or tempy>=421):
                tempy=tempy+1
            if((not(1 in tmap1[tempx-3:tempx+2,tempy-3:tempy+2])) and \
               tmap2[tempx-1,tempy-1]==0):
                [temppath,tagC]=find_path(startx,starty,tempx,tempy,tmap1,zm)
                if(tagC!=2):
                    spath.append([tempx,tempy])
                    Spath.append(temppath)
                    lpath.append([len(temppath)-1,p])
                    e=e+1
        p=p+1

    #搜索成功，返回所有合适位置坐标
    o=0
    if(e>0):
        print(lpath[0][0],lpath[0][1])
        wx=spath[0][0]
        wy=spath[0][1]
        wp=Spath[0]
        if(lpath[0][0]>lpath[0][1]):
            for t in range(len(spath)):
                if(spath[0][0]==spath[t][0] and spath[0][1]==spath[t][1] and lpath[t][0]<=lpath[t][1]):
                    wx=spath[t][0]
                    wy=spath[t][1]
                    wp=Spath[t]
                    print(lpath[0][0],lpath[0][1])
                    o=1
                    break
            if(o==0):
                print("搜寻失败",startx,starty,"周围没有合适的位置")
                return [],[],1
        #返回坐标值，路径，标志位
        return [wx,wy],wp[1::],0
    else:
        print("搜寻失败",startx,starty,"周围没有合适的位置")
        return [],[],1

#以总路径最后一点开始寻找一合适位置
#map_1为地图搜索合适位置，保证该位置map_2上风速正常
def getBack(tx,ty,tmap1,tmap2):
    i=0
    gx=0
    gy=0
    while(1):
        del Path[-1]
        i=i+1#记录往回搜寻次数
        tx=Path[-1][1]
        ty=Path[-1][0]
        print("往回搜寻",i,"次，坐标为：",tx,ty)
        
        if(not(1 in tmap2[tx-3:tx+2,ty-3:ty+2])):
            gx=tx
            gy=ty
            for g in range(i):
                Path.append([ty,tx])
            print("搜索成功,该点为路径上的点,坐标为:",tx,ty)
            break
        print("i",i)   
        [gt,tp,tagB]=searchLocation(tx,ty,i,tmap1,tmap2)
        #如果在周围找到合适位置
        if(tagB==0):
            gx=gt[0]
            gy=gt[1]
            print(i,len(tp),tp,)
            for b in tp:
                Path.append(b)
            for c in range(i-len(tp)):
                Path.append(Path[-1])
            print("搜索成功，该点为路径点周围",i,"步的点，坐标为:",gx,gy)
            break
        #如果搜索到了起点，则退出
        if(tx==city[0][0] and ty==city[0][1]):
            break
        
    #搜索成功，找到合适位置   
    if(tmap2[gx-1,gy-1]==0):
        return [gx,gy],0
    #搜索失败，找不到合适位置   
    else:
        return [0,0],1
    
#判断该点周围有没有点风速过高，上下左右，如果有返回1，没有返回0
def findOne(coorx,coory):
    if(nowTM[coorx-2,coory-1]==0 and nowTM[coorx-1,coory-2]==0 and \
              nowTM[coorx-1,coory]==0 and nowTM[coorx,coory-1]==0):
        return 0
    return 1
def findZero(coorx,coory):
    if(nowTM[coorx-2,coory-1]==1 and nowTM[coorx-1,coory-2]==1 and \
              nowTM[coorx-1,coory]==1 and nowTM[coorx,coory-1]==1):
        return 0
    return 1

#########################################################   
     
#0 142 328
#1 84 203
#2 199 371 
#3 140 234       
#4 236 241
#5 315 281 
#6 358 207
#7 363 237
#8 423 266
#9 125 375                                                                                                                                                                                                                                                                             
#10 189 274
#目的地1-10
cityID = 10
#日期6-10
dateID = 7
#3/10
city   = [[142,328],[84,203],[199,371],[140,234],[236,241],[315,281],\
            [358,207],[363,237],[423,266],[125,375],[189,274]]#城市坐标
startX,startY = city[0][0],city[0][1]#起点坐标 
endX  ,endY   = city[cityID][0],city[cityID][1]#终点坐标
liX    = []#存放路径X坐标列表
liY    = []#存放路径Y坐标列表
liH    = []#存放时间列表
Path   = []#总路径列表
timeH  = 3#起始小时
timeM  = 0#起始分钟

#读取地图,TM为0和1,RM为真值
TM_0=pd.read_csv('DATA\weather{0}_TM.csv'.format(dateID),header=None)
TM=TM_0.values
RM_0=pd.read_csv('DATA\weather{0}_RM.csv'.format(dateID),header=None)
RM=RM_0.values

#开始寻路，从3点到20点
h      = 3
while(h>=3 and h<=20):    
    print("当前时间h:",h)
    
    ##############################################################
    
    #本小时使用的三种地图（前、中、后）
    nowTM = TM[(548*(h-3)):(548*(h-2)),:]
    nowRM = RM[(548*(h-3)):(548*(h-2)),:]
    tm    = nowTM.copy()
    rm    = np.zeros((548,421))
    if(h>3):
        aboveTM=TM[(548*(h-4)):(548*(h-3)),:]
        #aboveRM=RM[(548*(h-4)):(548*(h-3)),:]
    else:
        aboveTM=nowTM
        #aboveRM=nowRM
    if(h<20):
        nextTM=TM[(548*(h-2)):(548*(h-1)),:]
        #nextRM=RM[(548*(h-2)):(548*(h-1)),:]
    else:
        nextTM=nowTM
        #nextRM=nowRM   
    
    #起点和终点距离很远，更改地图
    tm=np.zeros((548,421))
    tm[startX-31:startX+30,startY-31:startY+30]=nowTM[startX-31:startX+30,startY-31:startY+30].copy()
   
    #将终点直接置0！！！
    nowTM[endX-1,endY-1]=0
    tm[endX-1,endY-1]=0
    #打印起点终点周围信息
    printSE(nowTM,startX,startY,endX,endY)
    #weather=pd.DataFrame(nowTM)
    #weather.to_csv("date{0}_weather{1}.csv".format(dateID,h))
    #h=h+1
    ##############################################################

    #起点处风速过高
    if(nowTM[startX-1,startY-1]==1):
        print("起点风速过高")
        tX,tY=startX,startY
        #使用前一小时搜索，并保证当前小时该位置风速正常
        [at,tagA]=getBack(tX,tY,aboveTM,nowTM)
        #如果搜索成功，将该位置作为本次起点
        if(tagA==0):
            startX,startY = at[0],at[1]
            printSE(nowTM,startX,startY,endX,endY)
        else:
            if(nowTM[startX-1,startY-1]==1):
                print("起点仍旧风速过高")
            print("找不到合适的点作为本次起点！退出")
            break
    ##############################################################    
    #起点终点距离很近，且终点周围风速过高
    if(abs(startX-endX)<=30 and abs(startY-endY)<=30 and nowTM[endX-2,endY-1]==1 and \
       nowTM[endX,endY-1]==1 and nowTM[endX-1,endY-2]==1 and nowTM[endX-1,endY]==1):
        nX,nY = startX,startY
        f  = 1
        bn    = 0
        while(f==1):
            if(nextTM[nX-1,nY-1]==0):
                print("终点风速过高，等一个小时")
                f=0
                startX,startY=nX,nY
                #等一个小时
                for n in range(30):
                    Path.append(Path[-1])
                break
            print("终点风速过高，在起点周围搜索一合适点作为终点")
            [ap,Ap,tagD]=searchLocationB(nX,nY,30+bn,nowTM,nextTM)
            if(tagD==0):
                #如果能收到当前和下一小时风速正常的点
                f=0
                startX,startY=ap[0],ap[1]
                print("终点风速过高，走到",startX,startY)
                for b in Ap:
                    Path.append(b)
                for c in range(30-len(Ap)):
                    Path.append(Path[-1])
                break
            else:
            #如果搜索不到，说明当前小时起点错误，需要重新搜索起点
                print("终点风速过高，起点错误")
                del Path[-1]
                bn=bn+1
                #nX,nY=Path[-1][1],Path[-1][0]
                print("搜寻点坐标为：",nX,nY)
                
        h=h+1
        continue
        
    ##############################################################
    #当起点终点距离很近，且终点周围风速正常时，判断终点外围是否被风速过高位置围住
    if(abs(startX-endX)<=30 and abs(startY-endY)<=30 and \
       not(1 in nowTM[endX-2:endX+1,endY-2:endY+1])): 
        cX,cY   = endX,endY
        maxX,maxY = 0,0
        minX,minY = 999,999
        tagE = 1
        j    = 30
        while(findOne(cX,cY)==0):
            cX=cX-1
            cY=cY
            j=j-1
            if(j<=0 or cX<=0):
                tagE=0
                break
        if(cX>=endX-30):
            print("终点没有被围住")
            tagE=0
        #保存该边界点
        else:
            CX=cX-1
            CY=cY
            cX=cX-1
            cY=cY
            print("终点被围住了,向上搜索的边界点为：",CX,CY)
        while(tagE==1):
            print(cX,cY)
            if(findOne(cX-1,cY) and findZero(cX-1,cY)):#上
                cX=cX-1
                cY=cY
                if(cX>maxX):
                    maxX=cX
                if(cX<minX):
                    minX=cX   
                if(CX==cX and CX==cX):
                    break
                continue
            if(findOne(cX-1,cY-1) or findZero(cX-1,cY-1)):#左上
                cX=cX-1
                cY=cY-1
                if(cX>maxX):
                    maxX=cX
                if(cX<minX):
                    minX=cX
                if(cY>maxY):
                    maxY=cY
                if(cY<minY):
                    minY=cY
                if(CX==cX and CX==cX):
                    break
                continue
            if(findOne(cX,cY-1) or findZero(cX,cY-1)):#左
                cX=cX
                cY=cY-1
                if(cY>maxY):
                    maxY=cY
                if(cY<minY):
                    minY=cY
                if(CX==cX and CX==cX):
                    break
                continue
            if(findOne(cX-1,cY+1) and findZero(cX-1,cY+1)):#左下
                cX=cX-1
                cY=cY+1
                if(cX>maxX):
                    maxX=cX
                if(cX<minX):
                    minX=cX
                if(cY>maxY):
                    maxY=cY
                if(cY<minY):
                    minY=cY
                if(CX==cX and CX==cX):
                    break
                continue
            if(findOne(cX+1,cY) and findZero(cX+1,cY)):#下
                cX=cX+1
                cY=cY
                if(cX>maxX):
                    maxX=cX
                if(cX<minX):
                    minX=cX
                if(CX==cX and CX==cX):
                    break
                continue
            if(findOne(cX+1,cY+1) and findZero(cX+1,cY+1)):#右下
                cX=cX+1
                cY=cY+1
                if(cX>maxX):
                    maxX=cX
                if(cX<minX):
                    minX=cX
                if(cY>maxY):
                    maxY=cY
                if(cY<minY):
                    minY=cY
                if(CX==cX and CX==cX):
                    break
                continue
            if(findOne(cX,cY+1) and findZero(cX,cY+1)):#右
                cX=cX
                cY=cY+1
                if(cY>maxY):
                    maxY=cY
                if(cY<minY):
                    minY=cY
                if(CX==cX and CX==cX):
                    break
                continue
            if(findOne(cX-1,cY+1) and findZero(cX-1,cY+1)):#右上
                cX=cX-1
                cY=cY+1
                if(cX>maxX):
                    maxX=cX
                if(cX<minX):
                    minX=cX
                if(cY>maxY):
                    maxY=cY
                if(cY<minY):
                    minY=cY
                if(CX==cX and CX==cX):
                    break
                continue
        if(tagE==1):
            print("终点被围住了")    
            if(startX<maxX and startX>minX and startY<maxY and startY>minY):
                print("起点也被围住了")
            else:
                print("起点没被围住，等一个小时吧！")
                h=h+1
                continue
        
    #寻找路径
    #printSE(nowTM,startX,startY,endX,endY)
    [tempPath, flag]=find_path(startX,startY,endX,endY,tm,rm)
   
    #如果路径大于30，继续走
    if(flag==1):
        startX,startY=tempPath[30][1],tempPath[30][0]
        print("下次起点为:",startX,startY)
        #将该路径添加到总路径
        if(h!=3):
            Path.extend(tempPath[1:31])
        else:
            Path.extend(tempPath[0:31])   
   
    #如果路径小于30，退出循环
    if(flag==0):
        print("路径小于30，搜寻结束")
        Path.extend(tempPath[1::])
        break
    
    #如果没路
    if(flag==2):
        print("起点外围被风速过高位置围住,没有路")
        #搜寻一个下一小时风速正常的位置
        if(nextTM[startX-1,startY-1]==0):
            #原地等一个小时
            print("在起点等一个小时")
            for a in range(30):
                Path.append(Path[-1])
            h=h+1
            continue

        [mp,Mp,tagF]=searchLocation(startX,startY,30,nowTM,nextTM)
        if(tagF==0):
            startX,startY=mp[0],mp[1]
            print("从起点走到",startX,startY)
            for c in Mp:
                Path.append(c)
            for d in range(30-len(Mp)):
                Path.append(Path[-1])
        else:
            print("起点周围没有合适点，且不能在起点等待，起点错误")
            del Path[-1]
            startX,startY=Path[-1][1],Path[-1][0]
            continue
                      
    h=h+1

#寻路结束   
#将路径写入文件
file=pd.DataFrame(columns=['target','date','time','xid','yid'])

for l in Path:
    liX.append(l[1])
    liY.append(l[0])
for i in range(len(liX)):
    liH.append(str(timeH)+":"+str(timeM))
    timeM=timeM+2
    if(timeM==60):
        timeM=0
        timeH=timeH+1
        
file['target'] = [cityID]*len(liX)
file['date']   = [dateID]*len(liX)
file['xid']    = liX
file['yid']    = liY
file['time']   = liH
file.to_csv('结果0120\City{0}_Date{1}.csv'.format(cityID,dateID),\
            index=False,header=False)

