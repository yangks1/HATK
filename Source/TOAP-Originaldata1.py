import time

from memory_profiler import memory_usage

from Tool import DataProcessing as DP


def utility(pattern):
    """
    :param pattern: 输入的需要计算的模式例如：[["1002", "1003"]["1004"]]
    :return: 返回模式pattern的效用值u(pattern)
    """
    utilityValue = 0
    for itemSets in pattern:
        for item in itemSets:
            utilityValue += utilityTable[item]
    return utilityValue


def lenPattern(pattern):
    """
    计算模式pattern长度 ：pattern中项的个数

    :param pattern: 模式pattern
    :return: 模式pattern的长度：各项集中项数之和
    """
    lengthOfPattern = 0
    for itemSet in pattern:
        lengthOfPattern += len(itemSet)
    return lengthOfPattern


def sizePattern(pattern):
    """

    :param pattern: 模式pattern
    :return: 模式pattern的大小：项集个数
    """
    return len(pattern)


def sc(p):
    sss = []
    seid = 0
    for ss in dataTable:
        sss.append([])
        for ssss in ss:
            sss[seid].append(ssss[:])
        seid += 1
    if p == [['a', 'a']]:
        print(p)
    supportValue = 0
    i = 0
    for s in sss:
        while i < len(s):
            position = []
            j = 0
            while j < len(p) and i < len(s):
                if set(p[j]).issubset(set(s[i])):
                    for k in p[j]:
                        if k not in s[i]:
                            print(k)
                        s[i].remove(k)
                    position.append(i)
                    j += 1
                    i += 1
                else:
                    i += 1
            if j == len(p):
                supportValue += 1
                i = position[0] + 1
            else:
                break

    return supportValue


def auCalculate(pattern):
    supportValue = sc(pattern)
    msub = mtb(pattern)
    utilityValue = utility(pattern)
    length = lenPattern(pattern)
    averageUtility = (supportValue * utilityValue) / length
    return averageUtility, msub


def mtb(p):
    uv = utility(p)
    auv = uv / lenPattern(p)
    maxs = 0
    num = 0
    for s in dataTable:
        position = []
        flag = 1
        i = 0
        u = 0
        while i < len(s):
            j = 0
            while j < len(p) and i < len(s):
                if set(p[j]).issubset(set(s[i])):
                    position.append(i)
                    j += 1
                    i += 1
                else:
                    i += 1
            if j == len(p):
                break
            else:
                flag = 0
                break
        if not flag:
            continue
        i = position[-1] + 1
        num1 = 0
        while i < len(s):
            for k in s[i]:
                if utilityTable[k] > auv:
                    u += utilityTable[k]
                    num1 += 1
            i += 1
        if u > maxs:
            maxs = u
            num = num1
    allu = uv + maxs
    mtbv = sc(p) * allu / (lenPattern(p) + num)
    return mtbv


def maxuCalculate():
    """
    计算效用表中最大单个效用值

    :return: 效用表中最大的效用值
    """
    maxUtility = 0
    for item in utilityTable.keys():
        if utilityTable[item] > maxUtility:
            maxUtility = utilityTable[item]
    return maxUtility


def maubCalculate(patternPositionTemp):
    """
    计算最大平均效用上界maub

    :param patternPositionTemp: 模式pattern的出现位置纪录
    :return: maub（pattern）
    """
    supportValue = sc(patternPositionTemp)
    maxUtilityOfOne = maxuCalculate()
    maub = maxUtilityOfOne * supportValue
    return maub


def saveTopkPattern(pattern, au):
    global minau, ListsTemp, kValue
    lengthOfList = len(ListsTemp[0])
    if lengthOfList < kValue:
        indexTemp = 0
        while indexTemp < lengthOfList and ListsTemp[1][indexTemp] > au:
            indexTemp += 1
        ListsTemp[0].insert(indexTemp, pattern)
        ListsTemp[1].insert(indexTemp, au)
        if lengthOfList + 1 == kValue:
            minau = ListsTemp[1][kValue - 1]
    else:
        indexTemp = 0
        while indexTemp < lengthOfList and ListsTemp[1][indexTemp] > au:
            indexTemp += 1
        if indexTemp <= lengthOfList:
            ListsTemp[0].insert(indexTemp, pattern)
            ListsTemp[1].insert(indexTemp, au)
            ListsTemp[0].pop()
            ListsTemp[1].pop()
        minau = ListsTemp[1][kValue - 1]


def EP():
    global candidatePatternNum, minau
    patternInfor = cPIL[0]
    sizeOfPattern = len(patternInfor[0])
    # 序列扩展
    for item in allItemList[0]:
        index = allItemList[0].index(item) + 1
        # 得到newPattern
        newPattern = patternInfor[0][:]
        newPattern.append([item])
        # print(newPattern)
        candidatePatternNum += 1
        au, msub = auCalculate(newPattern)
        if msub > minau:
            if au > minau:
                saveTopkPattern(newPattern, au)
            cPIL.append([newPattern, index, msub])
    # 项集扩展
    for item in allItemList[0][patternInfor[1]:]:
        index = allItemList[0].index(item) + 1
        newPattern = patternInfor[0][:sizeOfPattern - 1]
        newPattern.append(patternInfor[0][sizeOfPattern - 1][:])
        newPattern[sizeOfPattern - 1].append(item)
        # print(newPattern)
        #
        candidatePatternNum += 1
        au, msub = auCalculate(newPattern)
        if msub > minau:
            if au > minau:
                saveTopkPattern(newPattern, au)
            cPIL.append([newPattern, index, msub])


def TOAPminer():
    # 保存高平均效用模式
    # 初始化变量
    global cPIL, allItemList, candidatePatternNum, minau

    for item in utilityTable.keys():
        length = len(allItemList[0])
        index = 0
        u = utilityTable[item]
        while length > index and allItemList[1][index] >= u:
            index = index + 1
        allItemList[0].insert(index, item)
        allItemList[1].insert(index, u)
    # 生成1-长度的序列
    for item in allItemList[0]:
        index = allItemList[0].index(item) + 1
        candidatePatternNum += 1
        pattern = [[item]]
        au, msub = auCalculate(pattern)
        if msub > minau:
            if au > minau:
                saveTopkPattern(pattern, au)
            cPIL.append([pattern, index, msub])
    while cPIL:
        msub = cPIL[0][2]
        if msub > minau:
            EP()
        cPIL.pop(0)


"""['../Data/MicroblogPCUUtility.txt', '../Data/MicroblogPCU.txt'],
          ['../Data/Online2Utility.txt', '../Data/Online-2.txt'],
          ['../Data/onlineUtilityTable.txt', '../Data/online-utility.txt'],
          ['../Data/Sds1-utility.txt', '../Data/Sds1.txt'],
          ['../Data/Sds2-utility.txt', '../Data/Sds2.txt'],
          ['../Data/Sds3-utility.txt', '../Data/Sds3.txt'],
          ['../Data/Sds4-utility.txt', '../Data/Sds4.txt'],
          ['../Data/creatDataUtility1.txt', '../Data/creatData1.txt'],
          ['../Data/creatDataUtility2.txt', '../Data/creatData2.txt'],
          ['../Data/creatDataUtility3.txt', '../Data/creatData3.txt'],
          ['../Data/creatDataUtility4.txt', '../Data/creatData4.txt']"""
if __name__ == '__main__':
    fn = [['../Data/onlineUtilityTable.txt', '../Data/online-utility.txt']]
    kL = [[1]]
    kValue = 0
    for kValue in kL:
        for i in range(0, len(fn)):
            utilityTable = DP.operateUtilityTableFile1(fn[i][0])
            dataTable = DP.operateDataFile2(fn[i][1])
            cPIL = []
            minau = 0
            ListsTemp = [[], []]
            allItemList = [[], []]
            candidatePatternNum = 0
            starTime = time.time()
            maxs = memory_usage(TOAPminer, max_usage=True)
            endTime = time.time()
            print("k = " + str(kValue) + ", " + fn[i][1])
            with open("../Result/TOAP-Original.txt", 'a') as f:
                f.write("\n----------------------------------------------------------------------\n")
                f.write("k = " + str(kValue) + ", " + fn[i][1] + "\n")
                f.write(str(maxs) + "\t" + str(endTime - starTime) + "\t" + str(candidatePatternNum) + "\n")
                f.write(str(ListsTemp))
