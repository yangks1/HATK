# 存储效用表
# 以字典形式存储
import time

utilityTable = {}

'''               读取效用表                  '''
def operateUtilityTableFile():
    with open("../Data/OnlineRetail1Dataset.txt", 'r') as f1:
        global utilityTable
        for i in f1.readlines():
            name = i.split('\t', 1)[0]
            price = float(i.split('\t', 1)[1])
            utilityTable[name] = price
            # utilityTable[name] = []
            # utilityTable[name].append(price)


'''               预处理数据库                 '''
# dataTable存储各编号在各序列各项集中出现的位置
# 例如字符‘10002’在第一个序列第二、三个项集中出现，且在第二个序列第一个项集中出现，
# 则记录为{"10002":{"1":[2,3], "2": [1],"maub" :  }}
dataTable = {}  # 在一个字典中存储数据库信息;
# multiDataTable只存储各编号在多项集中的出现
multiDataTable = {}


def operateDataFile():  # 处理序列数据库
    global dataTable
    global multiDataTable
    for utk in utilityTable.keys():
        dataTable[utk] = {}
    for utk in utilityTable.keys():
        multiDataTable[utk] = {}
    with open("../Data/OnlineRetail1DatasetUtility.txt", 'r') as f2:
        # global dataTable
        r = 0  # 纪录序列号
        for j in f2.readlines():
            # 在dataTable中每个字符列表中添加一个列表纪录该字符在该序列中出现的位置
            # for dTK in dataTable.keys():
            #     dataTable[dTK].append([])
            strs = ""  # 用于记录读取出的字符串
            l = 0  # 纪录项号 项号从1开始
            flag = 0  # 用于纪录一个项集中多少项
            strs1 = str(r) + ""  # 用于将序列号改成字符串类型
            strs2 = ""  # 存储上一个编号数据
            for k in j:
                # 各编号数据之间用空格间隔
                if k != " " and strs != "-1":
                    strs = strs + k
                elif strs == "-1":  # 判断该数据是否为"-1"，如果是，代表该多项集结束
                    if flag == 1:  # 删除单项集位置，保证multiDataTable字典中存储的均是多项集信息
                        multiDataTable[strs2][strs1].remove(l)
                    flag = 0
                    l = l + 1
                    strs = ""
                # 如果字符k不是空格则继续扫描j，字符串str也不是“-1”，继续扫描字符串， 并将字符k加入字符串str中
                elif k == " ":
                    if strs not in dataTable.keys():
                        print(strs + "不存在")
                    elif strs1 not in multiDataTable[strs].keys():
                        dataTable[strs][strs1] = []
                        dataTable[strs][strs1].append(l)
                        multiDataTable[strs][strs1] = []
                        multiDataTable[strs][strs1].append(l)
                    elif strs1 not in dataTable[strs].keys():
                        dataTable[strs][strs1] = []
                        dataTable[strs][strs1].append(l)
                        if l not in multiDataTable[strs][strs1]:
                            multiDataTable[strs][strs1].append(l)
                    else:
                        if l not in dataTable[strs][strs1]:
                            dataTable[strs][strs1].append(l)
                        if l not in multiDataTable[strs][strs1]:
                            multiDataTable[strs][strs1].append(l)
                    strs2 = strs
                    strs = ""
                    flag = flag + 1
            r = r + 1  # 每扫描f2文件一行，代表一个序列，并且序列号+1
operateUtilityTableFile()
operateDataFile()
# print(dataTable)
for k in dataTable.keys():
    if k == "10002":
        print(dataTable[k])

# for kValue in multiDataTable.keys():
#     if kValue == "22086":
#         print(multiDataTable[kValue])



'''                        排序编号表                     '''
# 预用编号表
orderedUtilityTable = []

# 插入排序
# def orderingUtilityTable():
#     for codeName in utilityTable.keys():
#         if codeName not in orderedUtilityTable:
#             if orderedUtilityTable:
#                 index = 0
#                 for i in orderedUtilityTable:
#                     index = index + 1
#                     if utilityTable[codeName] > utilityTable[i]:
#                         orderedUtilityTable.insert(orderedUtilityTable.index(i), codeName)
#                         break
#                     if index == len(orderedUtilityTable):
#                         orderedUtilityTable.append(codeName)
#                         break
#             else:
#                 orderedUtilityTable.append(codeName)

# 冒泡排序
# def orderingUtilityTable():
#     for codeName in utilityTable.keys():
#         orderedUtilityTable.append(codeName)
#     swap = 1  # 用于纪录交换次数
#     while swap:
#         swap = 0
#         for i in range(0, len(orderedUtilityTable)-1):
#             if utilityTable[orderedUtilityTable[i]] < utilityTable[orderedUtilityTable[i + 1]]:
#                 orderedUtilityTable[i], orderedUtilityTable[i + 1] =orderedUtilityTable[i + 1], orderedUtilityTable[i]
#                 swap = swap + 1

# 选择排序
# def orderingUtilityTable():
#     for codeName in utilityTable.keys():
#         orderedUtilityTable.append(codeName)
#
#     for index1 in range(0, len(orderedUtilityTable)-1):
#         maxCodeIndex = index1
#         for index2 in range(index1 + 1, len(orderedUtilityTable)):
#             if utilityTable[orderedUtilityTable[index2]] > utilityTable[orderedUtilityTable[maxCodeIndex]]:
#                 maxCodeIndex = index2
#
#
#         orderedUtilityTable[index1], orderedUtilityTable[maxCodeIndex] =orderedUtilityTable[maxCodeIndex], orderedUtilityTable[index1]
#

# 希尔排序 非递归
# def orderingUtilityTable():
#     for codeName in utilityTable.keys():
#         orderedUtilityTable.append(codeName)
#     # 步长值
#     length = len(orderedUtilityTable)
#     gap = length // 2
#     while gap:
#         for index1 in range(0, gap):
#             while index1 < length - gap and utilityTable[orderedUtilityTable[index1]] < utilityTable[orderedUtilityTable[index1 + gap]]:
#                 orderedUtilityTable[index1], orderedUtilityTable[index1 + gap] = orderedUtilityTable[index1 + gap], orderedUtilityTable[index1]
#                 index1 = index1 + gap
#         gap = gap // 2

# 希尔排序 递归
for codeName in utilityTable.keys():
    orderedUtilityTable.append(codeName)
def orderingUtilityTable():
    # 步长值
    length = len(orderedUtilityTable)
    gap = length // 2
    while gap:
        for index1 in range(0, gap):
            while index1 < length - gap and utilityTable[orderedUtilityTable[index1]] < utilityTable[orderedUtilityTable[index1 + gap]]:
                orderedUtilityTable[index1], orderedUtilityTable[index1 + gap] = orderedUtilityTable[index1 + gap], orderedUtilityTable[index1]
                index1 = index1 + gap
        gap = gap // 2

# 测试使用
# operateUtilityTableFile()
# orderingUtilityTable()
# t = []
# for i in orderedUtilityTable:
#     t.append(utilityTable[i])
# print(t)
# print(orderedUtilityTable)
# print(len(orderedUtilityTable))





