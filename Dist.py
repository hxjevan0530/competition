# -*- coding: utf-8 -*-

#使用worst_fit方法在物理机中分配虚拟机
def distribute(pCoreNumber, pMemoryNumber, VMNumber, predictList, VMID, vmMem, vmCore, considerRe):
    pCore    = [pCoreNumber]#物理机内存大小列表
    pMemory  = [pMemoryNumber]#物理机内存大小列表
    result_1 = []
    List     = []
    ListB    = []
    flag     = 0
    flag_1   = 0
    
    for i in range(VMNumber):
        List.append(predictList[VMID[i]-1])
        ListB.append(0)    

    while(1):

        flag=0
        for i in range(VMNumber):
            if(List[i]==0 and ListB[i]==0):
                flag=flag+1
        if(flag==VMNumber):
            print('List is 0')
            break
        
        print('List',List)
        newVMMem=[]
        newVMCore=[]
        for i in range(VMNumber):
            newVMMem.append(List[i]*vmMem[i])
            newVMCore.append(List[i]*vmCore[i])
        print('newVMMem',newVMMem)
        print('newVMCore',newVMCore)

        if(considerRe==0):#MEM
            pMMax   = max(pMemory)
            vmMax   = max(newVMMem)
            pIndex  = pMemory.index(pMMax)
            vmIndex = newVMMem.index(vmMax)
        if(considerRe==1):#CPU
            pMMax   = max(pCore)
            vmMax   = max(newVMCore)
            pIndex  = pCore.index(pMMax)
            vmIndex = newVMCore.index(vmMax)
        print('pMMax',pMMax,'vmMax',vmMax,'pIndex',pIndex,'vmIndex',vmIndex)

        #虚拟机内存最大虚拟机核心数也应满足条件
        print(pMemory[pIndex],newVMMem[vmIndex],pCore[pIndex],newVMCore[vmIndex])
        if(pMemory[pIndex]>=newVMMem[vmIndex] and pCore[pIndex]>=newVMCore[vmIndex] and \
           newVMMem[vmIndex]!=0 and newVMCore[vmIndex]!=0):
            print('vm',vmIndex+1,'->','pc',pIndex+1)
            result_1.append([pIndex+1,'flavor'+str(VMID[vmIndex]),int(List[vmIndex])])
            List[vmIndex]=0
            pMemory[pIndex] = pMemory[pIndex]-newVMMem[vmIndex]
            pCore[pIndex]   = pCore[pIndex]-newVMCore[vmIndex] 
            print('pMemory',pMemory,'pCore',pCore)
            for i in range(VMNumber):
                List[i]=List[i]+ListB[i]
                ListB[i]=0
            print('List',List)
        elif(List[vmIndex]>=2):#一直减少虚拟机，数量都为0时增加一台物理机
            List[vmIndex]=List[vmIndex]-1 
            ListB[vmIndex]=ListB[vmIndex]+1
            continue
        #当虚拟机数量列表全为0时，增加一台物理机
        else:
            pMemory.append(pMemoryNumber)
            pCore.append(pCoreNumber)
            print('add a pc')
            for i in range(VMNumber):
                List[i]=List[i]+ListB[i]
                ListB[i]=0
            continue
    return flag_1, result_1, pMemory

