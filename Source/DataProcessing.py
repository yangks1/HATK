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



# 二、蛋白质单项集数据
def operateUtilityTableFile2():
    """
    蛋白质单项集数据

    :return:
    """
    with open("../Data/proteinUtility.txt", 'r') as f1:
        utilityTable = {}
        for i in f1.readlines():
            name = i.split('\t', 1)[0]
            price = float(i.split('\t', 1)[1])
            utilityTable[name] = price
    return utilityTable



def operateDataFile2(utilityTable):  # 处理序列数据库
    dataTableTemp = {}
    for uTT in utilityTable.keys():
        dataTableTemp[uTT] = {}
    with open("../Data/protein.txt", 'r') as f2:
        sequenceId = 0  # 纪录序列号
        for sequence in f2.readlines():
            if sequenceId == 1:
                break
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
                elif letter == " " and string:
                    if string not in dataTableTemp.keys():
                        print(1)
                        print(string)
                        print(string + "不存在")
                        print(2)
                    elif sequenceIdString not in dataTableTemp[string].keys():
                        dataTableTemp[string][sequenceIdString] = [[itemSetsId]]
                    else:
                        if itemSetsId not in dataTableTemp[string][sequenceIdString][0]:
                            dataTableTemp[string][sequenceIdString][0].append(itemSetsId)
                    string = ""
            sequenceId = sequenceId + 1  # 每扫描f2文件一行，代表一个序列，并且序列号+1

    return dataTableTemp


# 三、创建的随机数据集
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


