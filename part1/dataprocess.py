
# import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
import math
import random


# 定义函数
def ReadMyCsv(SaveList, fileName):
    csv_reader = csv.reader(open(fileName))
    for row in csv_reader:  # 把每个rna疾病对加入OriginalData，注意表头
        SaveList.append(row)
    return

def storFile(data, fileName):
    with open(fileName, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
    return


OriginalData = []
ReadMyCsv(OriginalData, "./original data/miRNADisease.csv")
print(len(OriginalData))

mesh = np.loadtxt("./original data/MeshID_original_wholeAfterDuplicate.txt", dtype=str, delimiter=";")  # 读取源文件
print('mesh长度', len(mesh))


# 预处理
# 小写OriginalData
counter = 0
while counter < len(OriginalData):
    OriginalData[counter][0] = OriginalData[counter][0].lower()
    OriginalData[counter][1] = OriginalData[counter][1].lower()
    counter = counter + 144
print('小写OriginalData')
# 小写mesh
print(type(mesh))
counter = 0
while counter < len(mesh):
    mesh[counter][0] = mesh[counter][0].lower()
    mesh[counter][1] = mesh[counter][1].lower()
    counter = counter + 1
print('小写mesh')


#去掉原数据中的'N/A'，有些数据互相对立，不能先去重
LncDisease = []
counter = 0
while counter < len(OriginalData):
    if OriginalData[counter][2] != 'n/a':
        Pair = []
        Pair.append(OriginalData[counter][0])
        Pair.append(OriginalData[counter][1])
        LncDisease.append(Pair)
    counter = counter + 1
print('LncDisease长度', len(LncDisease))
print('OriginalData长度', len(OriginalData))


# LncDisease去重，数据集有问题
NewLncDisease = []
counter = 0
while counter < len(LncDisease):
    flag = 0
    counter1 = 0
    while counter1 < len(NewLncDisease):
        if (LncDisease[counter][0] == NewLncDisease[counter1][0]) & (LncDisease[counter][1] == NewLncDisease[counter1][1]):
            flag = 1
            break
        counter1 = counter1 + 1
    if flag == 0:
        NewLncDisease.append(LncDisease[counter])
    counter = counter + 1
LncDisease = []
LncDisease = NewLncDisease
print('去重LncDisease')
print('LncDisease长度', len(LncDisease))
storFile(LncDisease, './result/LncDisease.csv')


# # mesh去重
# NewMesh = []
# BadMesh = []
# counter = 0
# while counter < len(mesh):
#     counter1 = 0
#     while counter1 < len(NewMesh):
#         if (mesh[counter][0] == NewMesh[counter1][0]) & (mesh[counter][1] == NewMesh[counter1][1]):
#             BadMesh.append(NewMesh[counter1])
#             break
#         counter1 = counter1 + 1
#     if counter1 == len(NewMesh):
#         NewMesh.append(mesh[counter])
#     counter = counter + 1
# mesh = []
# mesh = NewMesh
# print('去重mesh')
# print('mesh长度', len(mesh))
# print('BadMesh长度', len(BadMesh))
# text_save(mesh, '去重mesh.txt')
# text_save(BadMesh, 'BadMesh.txt')


# 构建AllDisease
AllDisease = []
counter1 = 0
while counter1 < len(OriginalData): #顺序遍历原始数据，构建AllDisease
    counter2 = 0
    flag = 0
    while counter2 < len(AllDisease):  #遍历AllDisease
        if OriginalData[counter1][1] != AllDisease[counter2]:#有新疾病
            counter2 = counter2 + 1
        elif OriginalData[counter1][1] == AllDisease[counter2]:#没有新疾病，用两个if第二个if会越界
            flag = 1
            counter2 = counter2 + 1
    if flag == 0:
        AllDisease.append(OriginalData[counter1][1])
    counter1 = counter1 + 1
print('len(AllDisease)', len(AllDisease))
storFile(AllDisease, './result/AllDisease.csv')


# 构建AllRNA
AllRNA = []
counter1 = 0
while counter1 < len(OriginalData): #顺序遍历原始数据，构建AllDisease
    counter2 = 0
    flag = 0
    while counter2 < len(AllRNA):  #遍历AllDisease
        if OriginalData[counter1][0] != AllRNA[counter2]:#有新疾病
            counter2 = counter2 + 1
        elif OriginalData[counter1][0] == AllRNA[counter2]:#没有新疾病，用两个if第二个if会越界
            flag = 1
            break
    if flag == 0:
        AllRNA.append(OriginalData[counter1][0])
    counter1 = counter1 + 1
print('len(miAllRNA)', len(AllRNA))
storFile(AllRNA, './result/miAllRNA.csv')


# 构建disease idGroup，有对应id的生成id group，没有的加入[0]
DiseaseAndMeshID = []
counter1 = 0
while counter1 < len(AllDisease):
    DiseaseAndMeshPair = []
    DiseaseAndMeshID.append(DiseaseAndMeshPair)
    DiseaseAndMeshID[counter1].append(AllDisease[counter1])
    counter2 = 0
    flag = 0
    while counter2 < len(mesh):#遍历整个mesh，寻找相同疾病的所有id
        if (mesh[counter2][0] == DiseaseAndMeshID[counter1][0]) & (flag == 1):#加入
            DiseaseAndMeshID[counter1][1].append(mesh[counter2][1])
        if (mesh[counter2][0] == DiseaseAndMeshID[counter1][0]) & (flag == 0):#新建mesh id 列表
            MeshID = []
            MeshID.append(mesh[counter2][1])
            DiseaseAndMeshID[counter1].append(MeshID)
            flag = 1
        if (counter2 == len(mesh) - 1) & (len(DiseaseAndMeshID[counter1]) == 1):    # 当遍历到最后一个长度仍为1，增加一个0
            DiseaseAndMeshID[counter1].append(0)
        counter2 = counter2 + 1
    counter1 = counter1 + 1
print('DiseaseAndMeshID')
print(len(DiseaseAndMeshID))
storFile(DiseaseAndMeshID, './result/DiseaseAndMeshID.csv')


# 由rna-disease生成对应关系矩阵，有关系1，没关系0，行为疾病AllDisease，列为rna AllRNA
# 生成全0矩阵
DiseaseAndRNABinary = []
counter = 0
while counter < len(AllDisease):
    row = []
    counter1 = 0
    while counter1 < len(AllRNA):
        row.append(0)
        counter1 = counter1 + 1
    DiseaseAndRNABinary.append(row)
    counter = counter + 1


print('len(LncDisease)', len(LncDisease))
counter = 0
while counter < len(LncDisease):
    DN = LncDisease[counter][1]     # disease name
    RN = LncDisease[counter][0]     # rna name
    counter1 = 0
    while counter1 < len(AllDisease):
        if AllDisease[counter1] == DN:
            counter2 = 0
            while counter2 < len(AllRNA):
                if AllRNA[counter2] == RN:
                    DiseaseAndRNABinary[counter1][counter2] = 1
                    break
                counter2 = counter2 + 1
            break
        counter1 = counter1 + 1
    counter = counter + 1
print('len(DiseaseAndRNABinary)', len(DiseaseAndRNABinary))
storFile(DiseaseAndRNABinary, './result/DiseaseAndRNABinary.csv')


# 构建疾病的DAGs
# 构建dags的根节点
DAGs = []
counter1 = 0
while counter1 < len(AllDisease):
    group = []
    group.extend(DiseaseAndMeshID[counter1])
    group.append(0)
    group1 = []
    group1.append(group)
    DAGs.append(group1)
    counter1 = counter1 + 1
print('len(DAGs)的叶子', len(DAGs))
storFile(DAGs, './result/DAGsLeaf.csv')


# if DAGs[0][0][1] == 0:
#     print('ok')
# else:
#     print('nook')
# 生成AllDisease的完整DGAs[[[RootDisease,[ID,ID],layer],[FatherDisease,[ID,ID],layer]...],...]
counter = 0
while counter < len(DAGs):
    if DAGs[counter][0][1] == 0:
        counter = counter + 1
        continue
    counter1 = 0
    while counter1 < len(DAGs[counter]):  #################
        counter2 = 0
        while counter2 < len(DAGs[counter][counter1][1]):  ###################只对一个节点扩展只能生成的二层信息
            layer = DAGs[counter][counter1][2]  #######################
            # if len(DAGs[0][counter1][1][counter2]) <= 3:
            #     break
            if len(DAGs[counter][counter1][1][counter2]) > 3:  ####################
                NID = DAGs[counter][counter1][1][counter2]  #####################
                L = len(NID)
                NID = NID[0:L - 4]  # 把id减3
                counter3 = 0
                flag = 1  # 默认不在
                while counter3 < len(mesh):  # 判断nid是否在mesh中，如果在求出疾病名，如果不在，跳出循还
                    if NID == mesh[counter3][1]:
                        flag = 0  # 由counter3找对应的疾病名
                        num = counter3
                        DiseaseName = mesh[counter3][0]
                        break
                    counter3 = counter3 + 1

                flag2 = 0  # 默认在dags不存在
                counter5 = 0
                while counter5 < len(DAGs[counter]):  # 找到对应疾病的名字后查找dags看是否已经出现，出现了就不加了
                    if DAGs[counter][counter5][0] == DiseaseName:  #########################
                        flag2 = 1  # dags中出现了
                        break
                    counter5 = counter5 + 1

                if flag == 0:
                    if flag2 == 0:
                        counter6 = 0    # 遍历mesh，寻找disease对应的id
                        IDGroup = []
                        while counter6 < len(mesh):
                            if DiseaseName == mesh[counter6][0]:
                                IDGroup.append(mesh[counter6][1])
                            counter6 = counter6 + 1
                        DiseasePoint = []
                        layer = layer + 1
                        DiseasePoint.append(DiseaseName)
                        DiseasePoint.append(IDGroup)
                        DiseasePoint.append(layer)
                        DAGs[counter].append(DiseasePoint)  ######################

            counter2 = counter2 + 1
        counter1 = counter1 + 1
    counter = counter + 1
print('DAGs', len(DAGs))
storFile(DAGs, './result/DAGs.csv')


# 构建model1
# 构建DV(disease value)，通过AllDisease构建的DiseaseAndMesh和DAGs，所以疾病顺序都一样，通过dags的layer构建DiseaseValue
DiseaseValue = []
counter = 0
while counter < len(AllDisease):
    if DAGs[counter][0][1] == 0:
        DiseaseValuePair = []
        DiseaseValuePair.append(AllDisease[counter])
        DiseaseValuePair.append(0)
        DiseaseValue.append(DiseaseValuePair)
        counter = counter + 1
        continue
    counter1 = 0
    DV = 0
    while counter1 < len(DAGs[counter]):
        DV = DV + math.pow(0.5, DAGs[counter][counter1][2])
        counter1 = counter1 + 1
    DiseaseValuePair = []
    DiseaseValuePair.append(AllDisease[counter])
    DiseaseValuePair.append(DV)
    DiseaseValue.append(DiseaseValuePair)
    counter = counter + 1
print('len(DiseaseValue)', len(DiseaseValue))
storFile(DiseaseValue, './result/DiseaseValue.csv')


# 生成两个疾病DAGs相同部分的DV
SameValue1 = []
counter = 0
while counter < len(AllDisease):
    RowValue = []
    if DiseaseValue[counter][1] == 0:           # 没有mesh id，整行都为0
        counter1 = 0
        while counter1 < len(AllDisease):
            RowValue.append(0)
            counter1 = counter1 + 1
        SameValue1.append(RowValue)
        counter = counter + 1
        continue
    counter1 = 0
    while counter1 < len(AllDisease):#疾病counter和疾病counter1之间的共同节点
        if DiseaseValue[counter1][1] == 0:  # 没有mesh id，此点为0
            RowValue.append(0)
            counter1 = counter1 + 1
            continue
        DiseaseAndDiseaseSimilarityValue = 0
        counter2 = 0
        while counter2 < len(DAGs[counter]):#疾病counter的所有DAGs的节点
            counter3 = 0
            while counter3 < len(DAGs[counter1]):#疾病counter1的所有DAGs的节点
                if DAGs[counter][counter2][0] == DAGs[counter1][counter3][0]:#找出共同节点
                    DiseaseAndDiseaseSimilarityValue = DiseaseAndDiseaseSimilarityValue + math.pow(0.5, DAGs[counter][counter2][2]) + math.pow(0.5, DAGs[counter1][counter3][2]) #自己和自己的全部节点相同，对角线即DiseaseValue的两倍
                counter3 = counter3 + 1
            counter2 = counter2 + 1
        RowValue.append(DiseaseAndDiseaseSimilarityValue)
        counter1 = counter1 + 1
    SameValue1.append(RowValue)
    counter = counter + 1
print('SameValue1')
storFile(SameValue1, './result/Samevalue1.csv')


# 生成model1
DiseaseSimilarityModel1 = []
counter = 0
while counter < len(AllDisease):
    RowValue = []
    if DiseaseValue[counter][1] == 0:           # 没有mesh id，整行都为0
        counter1 = 0
        while counter1 < len(AllDisease):
            RowValue.append(0)
            counter1 = counter1 + 1
        DiseaseSimilarityModel1.append(RowValue)
        counter = counter + 1
        continue
    counter1 = 0
    while counter1 < len(AllDisease):
        if DiseaseValue[counter1][1] == 0:  # 没有mesh id，此点为0
            RowValue.append(0)
            counter1 = counter1 + 1
            continue
        value = SameValue1[counter][counter1] / (DiseaseValue[counter][1] + DiseaseValue[counter1][1])
        RowValue.append(value)
        counter1 = counter1 + 1
    DiseaseSimilarityModel1.append(RowValue)
    counter = counter + 1
print('DiseaseSimilarityModel1，行数', len(DiseaseSimilarityModel1))
print('DiseaseSimilarityModel1[0]，列数', len(DiseaseSimilarityModel1[0]))
storFile(DiseaseSimilarityModel1, './result/DiseaseSimilarityModel1.csv')


# 构建model2
# 构建MeshAllDisease，mesh中的所有不相同疾病
MeshAllDisease = []
counter = 0
while counter < len(mesh):
    counter1 = 0
    flag = 0
    while counter1 < len(MeshAllDisease):
        if mesh[counter][0] == MeshAllDisease[counter1]:
            flag = 1
            break
        counter1 = counter1 + 1
    if flag == 0:
        MeshAllDisease.append(mesh[counter][0])
    counter = counter + 1
print('len(MeshAllDisease)', len(MeshAllDisease))
storFile(MeshAllDisease, './result/MeshAllDisease.csv')

# 构建MeshAllDiseaseAndMeshID
MeshAllDiseaseAndMeshID = []
counter1 = 0
while counter1 < len(MeshAllDisease):
    DiseaseAndMeshPair = []
    MeshAllDiseaseAndMeshID.append(DiseaseAndMeshPair)
    MeshAllDiseaseAndMeshID[counter1].append(MeshAllDisease[counter1])
    counter2 = 0
    flag = 0
    while counter2 < len(mesh):#遍历整个mesh，寻找相同疾病的所有id
        if (mesh[counter2][0] == MeshAllDiseaseAndMeshID[counter1][0]) & (flag == 1):#加入
            MeshAllDiseaseAndMeshID[counter1][1].append(mesh[counter2][1])
        if (mesh[counter2][0] == MeshAllDiseaseAndMeshID[counter1][0]) & (flag == 0):#新建mesh id 列表
            MeshID = []
            MeshID.append(mesh[counter2][1])
            MeshAllDiseaseAndMeshID[counter1].append(MeshID)
            flag = 1
        counter2 = counter2 + 1
    counter1 = counter1 + 1
print('len(MeshAllDiseaseAndMeshID)', len(MeshAllDiseaseAndMeshID))
storFile(MeshAllDiseaseAndMeshID, './result/MeshAllDiseaseAndMeshID.csv')

# 构建MeshAllDiseaseDAGs的根节点
MeshAllDiseaseDAGs = []
counter1 = 0
while counter1 < len(MeshAllDisease):
    group = []
    group.extend(MeshAllDiseaseAndMeshID[counter1])
    group.append(0)
    group1 = []
    group1.append(group)
    MeshAllDiseaseDAGs.append(group1)
    counter1 = counter1 + 1
print('./result/MeshAllDiseaselen(DAGs)的叶子', len(MeshAllDiseaseDAGs))


# 构建MeshAllDiseaseDAGs
counter = 0
while counter < len(MeshAllDiseaseDAGs):
    counter1 = 0
    while counter1 < len(MeshAllDiseaseDAGs[counter]):  #################
        counter2 = 0
        while counter2 < len(MeshAllDiseaseDAGs[counter][counter1][1]):  ###################只对一个节点扩展只能生成的二层信息
            layer = MeshAllDiseaseDAGs[counter][counter1][2]  #######################
            # if len(DAGs[0][counter1][1][counter2]) <= 3:
            #     break
            if len(MeshAllDiseaseDAGs[counter][counter1][1][counter2]) > 3:  ####################
                NID = MeshAllDiseaseDAGs[counter][counter1][1][counter2]  #####################
                L = len(NID)
                NID = NID[0:L - 4]  # 把id减3
                counter3 = 0
                flag = 1  # 默认不在
                while counter3 < len(mesh):  # 判断nid是否在mesh中，如果在求出疾病名，如果不在，跳出循还
                    if NID == mesh[counter3][1]:
                        flag = 0  # 由counter3找对应的疾病名
                        num = counter3
                        DiseaseName = mesh[counter3][0]
                        break
                    counter3 = counter3 + 1

                DiseaseName = mesh[num][0]
                flag2 = 0  # 默认在dags不存在
                counter5 = 0
                while counter5 < len(MeshAllDiseaseDAGs[counter]):  # 找到对应疾病的名字后查找dags看是否已经出现，出现了就不加了
                    if MeshAllDiseaseDAGs[counter][counter5][0] == DiseaseName:  #########################
                        flag2 = 1  # dags中出现了
                        break
                    counter5 = counter5 + 1

                if flag == 0:
                    if flag2 == 0:
                        counter6 = 0    # 遍历mesh，寻找disease对应的id
                        IDGroup = []
                        while counter6 < len(mesh):
                            if DiseaseName == mesh[counter6][0]:
                                IDGroup.append(mesh[counter6][1])
                            counter6 = counter6 + 1
                        DiseasePoint = []
                        layer = layer + 1
                        DiseasePoint.append(DiseaseName)
                        DiseasePoint.append(IDGroup)
                        DiseasePoint.append(layer)
                        MeshAllDiseaseDAGs[counter].append(DiseasePoint)  ######################

            counter2 = counter2 + 1
        counter1 = counter1 + 1
    print(counter)
    counter = counter + 1
print('len(MeshAllDiseaseDAGs)', len(MeshAllDiseaseDAGs))
storFile(MeshAllDiseaseDAGs, './result/MeshAllDiseaseDAGs.csv')

# 构建DiseaseFrequence，AllDisease在MeshAllDiseaseDAGs中出现的次数，可能为0次
DiseaseFrequence = []
counter = 0
while counter < len(AllDisease):
    num = 0
    counter1 = 0
    while counter1 < len(MeshAllDisease):#遍历所有疾病，疾病counter是否在疾病counter1中出现过
        counter2 = 0
        while counter2 < len(MeshAllDiseaseDAGs[counter1]):
            if AllDisease[counter] == MeshAllDiseaseDAGs[counter1][counter2][0]:
                num = num + 1
                break
            counter2 = counter2 + 1
        counter1 = counter1 + 1
    DiseaseFrequencePair = []
    DiseaseFrequencePair.append(AllDisease[counter])
    DiseaseFrequencePair.append(num)
    DiseaseFrequence.append(DiseaseFrequencePair)
    counter = counter + 1
print('len(DiseaseFrequence)', len(DiseaseFrequence))
storFile(DiseaseFrequence, './result/DiseaseFrequence.csv')


# 计算每个疾病dags中的对数和，model2的分母DV2

DAGsV = DAGs
print('DAGsV[0]',DAGsV[0])
from math import e
from math import log
DiseaseValue2 = []
counter = 0
while counter < len(DAGs):
    counter1 = 0
    while counter1 < len(DAGs[counter]):
        Value = 0
        DN = DAGs[counter][counter1][0]
        num = 0
        counter2 = 0
        while counter2 < len(MeshAllDiseaseDAGs):
            counter3 = 0
            while counter3 < len(MeshAllDiseaseDAGs[counter2]):
                if DN == MeshAllDiseaseDAGs[counter2][counter3][0]:
                    num = num + 1
                counter3 = counter3 + 1
            counter2 = counter2 + 1
        if num == 0:
            Value = 0
        if num != 0:
            Value = -log(num / len(MeshAllDiseaseDAGs), 2)
        DAGsV[counter][counter1].append(Value)
        counter1 = counter1 + 1
    SumValue = 0
    counter4 = 0
    while counter4 < len(DAGs[counter]):
        SumValue = SumValue + DAGs[counter][counter4][3]
        counter4 = counter4 + 1
    DAGsV[counter].append(SumValue)
    counter = counter + 1

print('DAGsV[0]',DAGsV[0])
storFile(DAGsV, './result/DAGsV.csv')


# DiseaseSimilarityModel2
DiseaseSimilarityModel2 = []
counter = 0
while counter < len(AllDisease):
    RowValue = []
    if DAGsV[counter][0][1] == 0:        # 无mesh id，无法形成dag，和其他所有disease相似度为0
        for i in range(len(AllDisease)):
            RowValue.append(0)
        DiseaseSimilarityModel2.append(RowValue)
        counter = counter + 1
        continue
    counter1 = 0
    while counter1 < len(AllDisease):   # 疾病counter和疾病counter1之间的共同节点
        if DAGsV[counter1][0][1] == 0:      # 无mesh id，无法形成dag，和其他所有disease相似度为0
            RowValue.append(0)
            counter1 = counter1 + 1
            continue
        DiseaseAndDiseaseSimilarityValue = 0        # 否则找共同部分
        counter2 = 0
        while counter2 < len(DAGsV[counter]) - 1:    # 疾病counter的所有DAGs的节点
            counter3 = 0
            while counter3 < len(DAGsV[counter1]) - 1:       # 疾病counter1的所有DAGs的节点
                DN1 = DAGsV[counter][counter2][1]
                DN2 = DAGsV[counter1][counter3][1]
                if DN1 == DN2:     # ?
                    DiseaseAndDiseaseSimilarityValue = DiseaseAndDiseaseSimilarityValue + DAGsV[counter][counter2][3] + DAGsV[counter1][counter3][3]
                counter3 = counter3 + 1
            counter2 = counter2 + 1
        DiseaseAndDiseaseSimilarityValue = DiseaseAndDiseaseSimilarityValue / (DAGsV[counter][len(DAGsV[counter]) - 1] + DAGsV[counter1][len(DAGsV[counter1]) - 1])
        RowValue.append(DiseaseAndDiseaseSimilarityValue)
        counter1 = counter1 + 1
    DiseaseSimilarityModel2.append(RowValue)
    print(counter)
    counter = counter + 1
storFile(DiseaseSimilarityModel2, './result/DiseaseSimilarityModel2.csv')



# 计算rd
counter1 = 0
sum1 = 0
while counter1 < (len(AllDisease)):
    counter2 = 0
    while counter2 < (len(AllRNA)):
        sum1 = sum1 + pow((DiseaseAndRNABinary[counter1][counter2]), 2)
        counter2 = counter2 + 1
    counter1 = counter1 + 1
print('sum1=', sum1)
Ak = sum1
Nd = len(AllDisease)
rdpie = 0.5
rd = rdpie * Nd / Ak
print('disease rd', rd)
# 生成DiseaseGaussian
DiseaseGaussian = []
counter1 = 0
while counter1 < len(AllDisease):#计算疾病counter1和counter2之间的similarity
    counter2 = 0
    DiseaseGaussianRow = []
    while counter2 < len(AllDisease):# 计算Ai*和Bj*
        AiMinusBj = 0
        sum2 = 0
        counter3 = 0
        AsimilarityB = 0
        while counter3 < len(AllRNA):#疾病的每个属性分量
            sum2 = pow((DiseaseAndRNABinary[counter1][counter3] - DiseaseAndRNABinary[counter2][counter3]), 2)#计算平方
            AiMinusBj = AiMinusBj + sum2
            counter3 = counter3 + 1
        AsimilarityB = math.exp(- (AiMinusBj/rd))
        DiseaseGaussianRow.append(AsimilarityB)
        counter2 = counter2 + 1
    DiseaseGaussian.append(DiseaseGaussianRow)
    counter1 = counter1 + 1
print('len(DiseaseGaussian)', len(DiseaseGaussian))
storFile(DiseaseGaussian, './result/DiseaseGaussian.csv')


# counter = 0
# AiMinusBj = 0
# print(DiseaseAndRNABinary[0])
# print(DiseaseAndRNABinary[8])
# while counter < len(AllRNA):
#     sum2 = pow((DiseaseAndRNABinary[0][counter] - DiseaseAndRNABinary[8][counter]), 2)  # 计算平方
#     AiMinusBj = AiMinusBj + sum2
#     counter = counter + 1
#
# AsimilarityB = math.exp(- (AiMinusBj / rd))
# print('AiMinusBj', AiMinusBj)
# print('AsimilarityB', AsimilarityB)

# 构建RNAGaussian
from numpy import *
MDiseaseAndRNABinary = np.array(DiseaseAndRNABinary)    # 列表转为矩阵
RNAAndDiseaseBinary = MDiseaseAndRNABinary.T    # 转置DiseaseAndMiRNABinary
RNAGaussian = []
counter1 = 0
sum1 = 0
while counter1 < (len(AllRNA)):     # rna数量
    counter2 = 0
    while counter2 < (len(AllDisease)):     # disease数量
        sum1 = sum1 + pow((RNAAndDiseaseBinary[counter1][counter2]), 2)
        counter2 = counter2 + 1
    counter1 = counter1 + 1
print('sum1=', sum1)
Ak = sum1
Nm = len(AllRNA)
rdpie = 0.5
rd = rdpie * Nm / Ak
print('RNA rd', rd)
# 生成RNAGaussian
counter1 = 0
while counter1 < len(AllRNA):   # 计算rna counter1和counter2之间的similarity
    counter2 = 0
    RNAGaussianRow = []
    while counter2 < len(AllRNA):   # 计算Ai*和Bj*
        AiMinusBj = 0
        sum2 = 0
        counter3 = 0
        AsimilarityB = 0
        while counter3 < len(AllDisease):   # rna的每个属性分量
            sum2 = pow((RNAAndDiseaseBinary[counter1][counter3] - RNAAndDiseaseBinary[counter2][counter3]), 2)#计算平方，有问题？？？？？
            AiMinusBj = AiMinusBj + sum2
            counter3 = counter3 + 1
        AsimilarityB = math.exp(- (AiMinusBj/rd))
        RNAGaussianRow.append(AsimilarityB)
        counter2 = counter2 + 1
    RNAGaussian.append(RNAGaussianRow)
    counter1 = counter1 + 1
print('type(miRNAGaussian)', type(RNAGaussian))
storFile(RNAGaussian, './result/miRNAGaussian.csv')