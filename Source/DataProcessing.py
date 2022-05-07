import random

# 一、线上系统完整数据集
def operateUtilityTableFile1():
    """
    线上系统完整数据集

    :return:
    """
    with open("../Data/onlineUtilityTable.txt", 'r') as f1:
        utilityTable = {}
        for i in f1.readlines():
            name = i.split('\t', 1)[0]
            price = float(i.split('\t', 1)[1])
            utilityTable[name] = price
    return utilityTable


# 预处理数据库
# 存储各编号在各序列各项集中出现的位置
# 例如字符‘10002’在第一个序列第二、三个项集中出现，且在第二个序列第一个项集中出现，
# 则记录为{"10002":{"1":[2,3], "2": [1]}}
def operateDataFile1(utilityTable):  # 处理序列数据库
    dataTableTemp = {}
    for uTT in utilityTable.keys():
        dataTableTemp[uTT] = {}
    with open("../Data/online-utility.txt", 'r') as f2:
        sequenceId = 0  # 纪录序列号
        for sequence in f2.readlines():
            string = ""  # 用于记录读取出的字符串
            itemSetsId = 0  # 纪录项号 项号从1开始
            sequenceIdString = str(sequenceId) + ""  # 用于将序列号改成字符串类型
            for letter in sequence:
                # 各编号数据之间用空格间隔
                if letter != " " and string != "-1":
                    string += letter
                elif string == "-1":  # 判断该数据是否为"-1"，如果是，代表该多项集结束
                    string = ""
                    itemSetsId += 1
                    # 如果字符k不是空格则继续扫描j，字符串str也不是“-1”，继续扫描字符串， 并将字符k加入字符串str中
                elif letter == " ":
                    if string not in dataTableTemp.keys():
                        print(string + "不存在")
                    elif sequenceIdString not in dataTableTemp[string].keys():
                        dataTableTemp[string][sequenceIdString] = [[itemSetsId]]
                    else:
                        if itemSetsId not in dataTableTemp[string][sequenceIdString][0]:
                            dataTableTemp[string][sequenceIdString][0].append(itemSetsId)
                    string = ""
            sequenceId = sequenceId + 1  # 每扫描f2文件一行，代表一个序列，并且序列号+1
    return dataTableTemp


# 二、创建的随机数据集
def operateUtilityTableFile3():
    """
    创建的随机数据集

    :return:
    """
    with open("../Data/creatDataUtility.txt", 'r') as f1:
        utilityTable = {}
        for i in f1.readlines():
            name = i.split('\t', 1)[0]
            price = float(i.split('\t', 1)[1])
            utilityTable[name] = price
    return utilityTable


def operateDataFile3(utilityTable):  # 处理序列数据库
    dataTableTemp = {}
    for uTT in utilityTable.keys():
        dataTableTemp[uTT] = {}
    with open("../Data/creatData.txt", 'r') as f2:
        sequenceId = 0  # 纪录序列号
        for sequence in f2.readlines():
            string = ""  # 用于记录读取出的字符串
            itemSetsId = 0  # 纪录项号 项号从1开始
            sequenceIdString = str(sequenceId) + ""  # 用于将序列号改成字符串类型
            for letter in sequence:
                # 各编号数据之间用空格间隔
                if letter != " " and string != "-1":
                    string += letter
                elif string == "-1":  # 判断该数据是否为"-1"，如果是，代表该多项集结束
                    string = ""
                    itemSetsId += 1
                    # 如果字符k不是空格则继续扫描j，字符串str也不是“-1”，继续扫描字符串， 并将字符k加入字符串str中
                elif letter == " ":
                    if string not in dataTableTemp.keys():
                        print(string + "不存在")
                    elif sequenceIdString not in dataTableTemp[string].keys():
                        dataTableTemp[string][sequenceIdString] = [[itemSetsId]]
                    else:
                        if itemSetsId not in dataTableTemp[string][sequenceIdString][0]:
                            dataTableTemp[string][sequenceIdString][0].append(itemSetsId)
                    string = ""
            sequenceId = sequenceId + 1  # 每扫描f2文件一行，代表一个序列，并且序列号+1
    return dataTableTemp


# 三、线上系统完整数据集
def operateUtilityTableOnline2():
    """
    Online-2

    :return:
    """
    with open("../Data/Online2Utility.txt", 'r') as f1:
        utilityTable = {}
        for i in f1.readlines():
            name = i.split('\t', 1)[0]
            price = float(i.split('\t', 1)[1])
            utilityTable[name] = price
    return utilityTable


def operateOnline2(utilityTable):  # 处理序列数据库
    dataTableTemp = {}
    for uTT in utilityTable.keys():
        dataTableTemp[uTT] = {}
    with open("../Data/Online-2.txt", 'r') as f2:
        sequenceId = 0  # 纪录序列号
        for sequence in f2.readlines():
            itemsets = sequence.split('-1')
            itemSetsId = 0  # 纪录项号 项号从1开始
            sequenceIdString = str(sequenceId) + ""  # 用于将序列号改成字符串类型
            if sequenceIdString == '':
                ii = 1
            for itemsetstr in itemsets:
                itemset = itemsetstr.split(' ')
                for item in itemset:
                    if "\n" in item:
                        item = item.replace("\n", '')
                    if item:
                        if sequenceIdString in dataTableTemp[item]:
                            if itemSetsId not in dataTableTemp[item][sequenceIdString]:
                                dataTableTemp[item][sequenceIdString][0].append(itemSetsId)
                        else:
                            dataTableTemp[item][sequenceIdString] = [[itemSetsId]]
                itemSetsId += 1
            sequenceId += 1
    return dataTableTemp


# 四、MicroblogPCU
def operateUtilityTableMicroblogPCU():
    """
    MicroblogPCU

    :return:
    """
    with open("../Data/MicroblogPCUUtility.txt", 'r') as f1:
        utilityTable = {}
        for i in f1.readlines():
            name = i.split('\t', 1)[0]
            price = float(i.split('\t', 1)[1])
            utilityTable[name] = price
    return utilityTable


def operateMicroblogPCU(utilityTable):  # 处理序列数据库
    dataTableTemp = {}
    for uTT in utilityTable.keys():
        dataTableTemp[uTT] = {}
    with open("../Data/MicroblogPCU.txt", 'r') as f2:
        sequenceId = 0  # 纪录序列号
        for sequence in f2.readlines():
            itemsets = sequence.split('-1')
            itemSetsId = 0  # 纪录项号 项号从1开始
            sequenceIdString = str(sequenceId) + ""  # 用于将序列号改成字符串类型
            if sequenceIdString == '':
                ii = 1
            for itemsetstr in itemsets:
                itemset = itemsetstr.split(' ')
                for item in itemset:
                    if "\n" in item:
                        item = item.replace("\n", '')
                    if "-" in item:
                        item = item.replace("-", '')
                    if item:
                        if sequenceIdString in dataTableTemp[item]:
                            if itemSetsId not in dataTableTemp[item][sequenceIdString]:
                                dataTableTemp[item][sequenceIdString][0].append(itemSetsId)
                        else:
                            dataTableTemp[item][sequenceIdString] = [[itemSetsId]]
                itemSetsId += 1
            sequenceId += 1
    for k in list(dataTableTemp.keys()):
        t = dataTableTemp[k]
        if t == {}:
            del(dataTableTemp[k])
    for u in list(utilityTable.keys()):
        if u not in dataTableTemp.keys():
            del (utilityTable[u])
    return dataTableTemp, utilityTable


def opChainstore_utility():
    u = {}
    d = {}

    with open("../Data/chainstore_utility.txt") as f3:
        sid = 0
        i = 0
        for s in f3.readlines():
            ss = s.split(":")
            ss1 = ss[0].split(" ")
            ss2 = ss[2].split(" ")
            for item in ss1:
                if item in u:
                    if item in d:
                        if sid in d[item]:
                            d[item][sid][0].append(i)
                        else:
                            d[item][sid] = [[]]
                            d[item][sid][0].append(i)
                    else:
                        d[item] = {}
                        d[item][sid] = [[]]
                        d[item][sid][0].append(i)
                else:
                    u[item] = float(ss2[ss1.index(item)])
                    d[item] = {}
                    d[item][sid] = [[]]
                    d[item][sid][0].append(i)
                i += 1
                j = random.randint(2, 6)
                if i > j:
                    i = 0
                    sid = sid + 1
    return u, d


# Sds1
def operateUTSds1():
    """
    Sds1

    :return:
    """
    with open("../Data/Sds1-utility.txt", 'r') as f1:
        utilityTable = {}
        for i in f1.readlines():
            name = i.split('\t', 1)[0]
            price = float(i.split('\t', 1)[1])
            utilityTable[name] = price
    return utilityTable


def operateSds1(utilityTable):  # 处理序列数据库
    dataTableTemp = {}
    for uTT in utilityTable.keys():
        dataTableTemp[uTT] = {}
    with open("../Data/Sds1.txt", 'r') as f2:
        sequenceId = 0  # 纪录序列号
        for sequence in f2.readlines():
            itemsets = sequence.split('-1')
            itemSetsId = 0  # 纪录项号 项号从1开始
            sequenceIdString = str(sequenceId) + ""  # 用于将序列号改成字符串类型
            if sequenceIdString == '':
                ii = 1
            for itemsetstr in itemsets:
                itemset = itemsetstr.split(' ')
                for item in itemset:
                    if "\n" in item:
                        item = item.replace("\n", '')
                    if item:
                        if sequenceIdString in dataTableTemp[item]:
                            if itemSetsId not in dataTableTemp[item][sequenceIdString]:
                                dataTableTemp[item][sequenceIdString][0].append(itemSetsId)
                        else:
                            dataTableTemp[item][sequenceIdString] = [[itemSetsId]]
                itemSetsId += 1
            sequenceId += 1
    for k in list(dataTableTemp.keys()):
        t = dataTableTemp[k]
        if t == {}:
            del(dataTableTemp[k])
    for u in list(utilityTable.keys()):
        if u not in dataTableTemp.keys():
            del (utilityTable[u])
    return dataTableTemp, utilityTable


# Sds2
def operateUTSds2():
    """
    Sds2

    :return:
    """
    with open("../Data/Sds2-utility.txt", 'r') as f1:
        utilityTable = {}
        for i in f1.readlines():
            name = i.split('\t', 1)[0]
            price = float(i.split('\t', 1)[1])
            utilityTable[name] = price
    return utilityTable


def operateSds2(utilityTable):  # 处理序列数据库
    dataTableTemp = {}
    for uTT in utilityTable.keys():
        dataTableTemp[uTT] = {}
    with open("../Data/Sds2.txt", 'r') as f2:
        sequenceId = 0  # 纪录序列号
        for sequence in f2.readlines():
            itemsets = sequence.split('-1')
            itemSetsId = 0  # 纪录项号 项号从1开始
            sequenceIdString = str(sequenceId) + ""  # 用于将序列号改成字符串类型
            if sequenceIdString == '':
                ii = 1
            for itemsetstr in itemsets:
                itemset = itemsetstr.split(' ')
                for item in itemset:
                    if "\n" in item:
                        item = item.replace("\n", '')
                    if item:
                        if sequenceIdString in dataTableTemp[item]:
                            if itemSetsId not in dataTableTemp[item][sequenceIdString]:
                                dataTableTemp[item][sequenceIdString][0].append(itemSetsId)
                        else:
                            dataTableTemp[item][sequenceIdString] = [[itemSetsId]]
                itemSetsId += 1
            sequenceId += 1
    for k in list(dataTableTemp.keys()):
        t = dataTableTemp[k]
        if t == {}:
            del(dataTableTemp[k])
    for u in list(utilityTable.keys()):
        if u not in dataTableTemp.keys():
            del (utilityTable[u])
    return dataTableTemp, utilityTable


# Sds3
def operateUTSds3():
    """
    Sds3

    :return:
    """
    with open("../Data/Sds3-utility.txt", 'r') as f1:
        utilityTable = {}
        for i in f1.readlines():
            name = i.split('\t', 1)[0]
            price = float(i.split('\t', 1)[1])
            utilityTable[name] = price
    return utilityTable


def operateSds3(utilityTable):  # 处理序列数据库
    dataTableTemp = {}
    for uTT in utilityTable.keys():
        dataTableTemp[uTT] = {}
    with open("../Data/Sds3.txt", 'r') as f2:
        sequenceId = 0  # 纪录序列号
        for sequence in f2.readlines():
            itemsets = sequence.split('-1')
            itemSetsId = 0  # 纪录项号 项号从1开始
            sequenceIdString = str(sequenceId) + ""  # 用于将序列号改成字符串类型
            if sequenceIdString == '':
                ii = 1
            for itemsetstr in itemsets:
                itemset = itemsetstr.split(' ')
                for item in itemset:
                    if "\n" in item:
                        item = item.replace("\n", '')
                    if item:
                        if sequenceIdString in dataTableTemp[item]:
                            if itemSetsId not in dataTableTemp[item][sequenceIdString]:
                                dataTableTemp[item][sequenceIdString][0].append(itemSetsId)
                        else:
                            dataTableTemp[item][sequenceIdString] = [[itemSetsId]]
                itemSetsId += 1
            sequenceId += 1
    for k in list(dataTableTemp.keys()):
        t = dataTableTemp[k]
        if t == {}:
            del(dataTableTemp[k])
    for u in list(utilityTable.keys()):
        if u not in dataTableTemp.keys():
            del (utilityTable[u])
    return dataTableTemp, utilityTable


# Sds4
def operateUTSds4():
    """
    Sds4

    :return:
    """
    with open("../Data/Sds4-utility.txt", 'r') as f1:
        utilityTable = {}
        for i in f1.readlines():
            name = i.split('\t', 1)[0]
            price = float(i.split('\t', 1)[1])
            utilityTable[name] = price
    return utilityTable


def operateSds4(utilityTable):  # 处理序列数据库
    dataTableTemp = {}
    for uTT in utilityTable.keys():
        dataTableTemp[uTT] = {}
    with open("../Data/Sds4.txt", 'r') as f2:
        sequenceId = 0  # 纪录序列号
        for sequence in f2.readlines():
            itemsets = sequence.split('-1')
            itemSetsId = 0  # 纪录项号 项号从1开始
            sequenceIdString = str(sequenceId) + ""  # 用于将序列号改成字符串类型
            if sequenceIdString == '':
                ii = 1
            for itemsetstr in itemsets:
                itemset = itemsetstr.split(' ')
                for item in itemset:
                    if "\n" in item:
                        item = item.replace("\n", '')
                    if item:
                        if sequenceIdString in dataTableTemp[item]:
                            if itemSetsId not in dataTableTemp[item][sequenceIdString]:
                                dataTableTemp[item][sequenceIdString][0].append(itemSetsId)
                        else:
                            dataTableTemp[item][sequenceIdString] = [[itemSetsId]]
                itemSetsId += 1
            sequenceId += 1
    for k in list(dataTableTemp.keys()):
        t = dataTableTemp[k]
        if t == {}:
            del(dataTableTemp[k])
    for u in list(utilityTable.keys()):
        if u not in dataTableTemp.keys():
            del (utilityTable[u])
    return dataTableTemp, utilityTable

def findUtility():
    u = {}
    with open("../Data/Sds1.txt", 'r') as f2:
        for sequences in f2.readlines():
            sequence = sequences.split(' ')
            for item in sequence:
                if item != '-1' and item != ' ' and item != '\n' and item != '\t'and "-" not in item:

                    if "\n" in item:
                        item = item.replace("\n", '')
                    if item not in u.keys():
                        u[item] = random.randint(1, 100000)/10
    # print(u)
    with open("../Data/Sds1-utility.txt", "w") as l:
        for i in u.keys():
            l.write(i + "\t" + str(u[i]) + "\n")

if __name__ == '__main__':
    findUtility()





# # 二、蛋白质单项集数据
# def operateUtilityTableFile2():
#     """
#     蛋白质单项集数据
#
#     :return:
#     """
#     with open("../Data/proteinUtility.txt", 'r') as f1:
#         utilityTable = {}
#         for i in f1.readlines():
#             name = i.split('\t', 1)[0]
#             price = float(i.split('\t', 1)[1])
#             utilityTable[name] = price
#     return utilityTable


# def operateDataFile2(utilityTable):  # 处理序列数据库
#     dataTableTemp = {}
#     for uTT in utilityTable.keys():
#         dataTableTemp[uTT] = {}
#     with open("../Data/protein.txt", 'r') as f2:
#         sequenceId = 0  # 纪录序列号
#         for sequence in f2.readlines():
#             if sequenceId == 1:
#                 break
#             string = ""  # 用于记录读取出的字符串
#             itemSetsId = 0  # 纪录项号 项号从1开始
#             sequenceIdString = str(sequenceId) + ""  # 用于将序列号改成字符串类型
#             for letter in sequence:
#                 # 各编号数据之间用空格间隔
#                 if letter != " " and string != "-1":
#                     string += letter
#                 elif string == "-1":  # 判断该数据是否为"-1"，如果是，代表该多项集结束
#                     string = ""
#                     itemSetsId += 1
#                     # 如果字符k不是空格则继续扫描j，字符串str也不是“-1”，继续扫描字符串， 并将字符k加入字符串str中
#                 elif letter == " " and string:
#                     if string not in dataTableTemp.keys():
#                         print(1)
#                         print(string)
#                         print(string + "不存在")
#                         print(2)
#                     elif sequenceIdString not in dataTableTemp[string].keys():
#                         dataTableTemp[string][sequenceIdString] = [[itemSetsId]]
#                     else:
#                         if itemSetsId not in dataTableTemp[string][sequenceIdString][0]:
#                             dataTableTemp[string][sequenceIdString][0].append(itemSetsId)
#                     string = ""
#             sequenceId = sequenceId + 1  # 每扫描f2文件一行，代表一个序列，并且序列号+1
#
#     return dataTableTemp

#

#
#
# def op():
#     d = []
#     with open("../Data/4.txt", 'r') as f2:
#
#         for sequence in f2.readlines():
#             sequence = sequence[:-6]
#             d.append(sequence)
#     with open("../Data/Sds4.txt", "w") as l:
#         for i in d:
#             l.write(i + "\n")



