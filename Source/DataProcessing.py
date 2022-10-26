import random

# 一、线上系统完整数据集
def operateUtilityTableFile1(fn):
    """
    线上系统完整数据集

    :return:wqqqqqq2
    """
    with open(fn, 'r') as f1:
        utilityTable = {}
        for i in f1.readlines():
            name = i.split('\t', 1)[0]
            # print(i)
            price = float(i.split('\t')[1])
            utilityTable[name] = price
    return utilityTable

# 预处理数据库
# 存储各编号在各序列各项集中出现的位置
# 例如字符‘10002’在第一个序列第二、三个项集中出现，且在第二个序列第一个项集中出现，
# 则记录为{"10002":{"1":[2,3], "2": [1]}}
def operateDataFile1(utilityTable, fn):  # 处理序列数据库
    dataTableTemp = {}
    for uTT in utilityTable.keys():
        dataTableTemp[uTT] = {}
    with open(fn, 'r') as f2:
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


def operateDataFile2(fn):  # 处理序列数据库
    dataTableTemp = []
    with open(fn, 'r') as f2:
        sequenceid = 0
        for sequence in f2.readlines():
            dataTableTemp.append([])
            sequence = sequence.split("\n")[0]
            sequenceL = sequence.split("-1")
            itemsetid = 0
            for itemset in sequenceL:
                dataTableTemp[sequenceid].append([])
                itemsetL = itemset.split(" ")
                for item in itemsetL:
                    if item and item != '-':
                        dataTableTemp[sequenceid][itemsetid].append(item)
                if dataTableTemp[sequenceid][itemsetid] is None:
                    dataTableTemp[sequenceid].pop(itemsetid)
                itemsetid += 1
            if dataTableTemp[sequenceid] is None:
                dataTableTemp.pop(sequenceid)
            sequenceid += 1
    return dataTableTemp


def findUtility():
    u = {}
    with open("../Data-remain/Sds1.txt", 'r') as f2:
        for sequences in f2.readlines():
            sequence = sequences.split(' ')
            for item in sequence:
                if item != '-1' and item != ' ' and item != '\n' and item != '\t'and "-" not in item:

                    if "\n" in item:
                        item = item.replace("\n", '')
                    if item not in u.keys():
                        u[item] = random.randint(1, 100000)/10
    # print(u)
    with open("../Data-remain/Sds1-utility.txt", "w") as l:
        for i in u.keys():
            l.write(i + "\t" + str(u[i]) + "\n")

if __name__ == '__main__':

    # str1 = "../Data/chainstoreUtility.txt"
    str2 = "../Data/chainstore.txt"
    # c = operateUtilityTableFile1(str1)
    b = operateDataFile2(str2)
    print(b)




#
# def op():
#     d = []
#     with open("../Data/4.txt", 'r') as f2:
#
#         for sequence in f2.readlines():
#             sequence = sequence[:-6]
#             d.append(sequence)
#     with open("../Data/DS10L1S6L8I5000F.txt", "w") as l:
#         for i in d:
#             l.write(i + "\n")

#
# def opChainstore_utility():
#     u = {}
#     d = []
#
#     with open("../Data/chainstore_utility.txt") as f3:
#         i = 0
#         s1 = ""
#         for s in f3.readlines():
#             ss = s.split(":")
#             ss1 = ss[0].split(" ")
#             ss2 = ss[2].split(" ")
#             for itemindex in range(0, len(ss1)):
#                 u[ss1[itemindex]] = float(ss2[itemindex])
#             s1 += ss[0] + " -1 "
#             i += 1
#             if i > random.randint(5, 8):
#                 s1 = s1[:-4]
#                 d.append(s1)
#                 i = 0
#                 s1 = ""
#
#
#     with open("../Data/chainstoreUtility.txt", "w") as f4:
#         for k in u.keys():
#             f4.write(k + "\t" + str(u[k]) + "\n")
#     with open("../Data/chainstore.txt", "w") as f5:
#         for k in d:
#             f5.write(k + "\n")
#     return u, d

