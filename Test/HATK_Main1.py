


# 存储效用表
# 以字典形式存储
import time

utilityTable = {}
def operateUtilityTableFile():
    with open("../Data/onlineUtilityTable.txt", 'r') as f1:
        global utilityTable
        for i in f1.readlines():
            name = i.split('\t', 1)[0]
            price = float(i.split('\t', 1)[1])
            utilityTable[name] = []
            utilityTable[name].append(price)


# dataTable存储各编号在各序列各项集中出现的位置
# 例如字符‘10002’在第一个序列第二、三个项集中出现，且在第二个序列第一个项集中出现，
# 则记录为{"10002":[[2,3][1]]}
dataTable = {}          # 在一个字典中存储数据库信息; 每个编号有一个二维列表{"10002":[[1,3][,4]] }
# multiDataTable只存储各编号在多项集中的出现
multiDataTable = {}
def operateDataFile():# 处理序列数据库
    global dataTable
    for utk in utilityTable.keys():
        dataTable[utk] = []
    with open("../Data/online-utility.txt", 'r') as f2:
        # global dataTable
        r = 0   # 纪录序列号

        for j in f2.readlines():
            # 在dataTable中每个字符列表中添加一个列表纪录该字符在该序列中出现的位置
            for dTK in dataTable.keys():
                dataTable[dTK].append([])
            str = ""   # 用于记录字符串
            l = 0  # 纪录项号 项号从0开始
            for k in j:
                # 各编号数据之间用空格间隔
                if k != " " and str != "-1":
                    str = str + k
                elif str == "-1":           # 判断该数据是否为"-1"，如果是，代表该多项集结束
                    l = l + 1
                    str = ""
                # 如果字符k不是空格则继续扫描j，字符串str也不是“-1”，继续扫描字符串， 并将字符k加入字符串str中
                elif k == " ":
                    if str not in dataTable.keys():
                        print(str + "不存在")
                    elif l not in dataTable[str][r]:
                        dataTable[str][r].append(l)
                    str = ""
            r = r + 1  # 每扫描f2文件一行，代表一个序列，并且序列号+1
operateDataFile()
operateUtilityTableFile()

for d in dataTable:
    i = 0
    while i < 10:
        print(d)


