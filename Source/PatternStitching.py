import time

from memory_profiler import memory_usage

from Tool import DataProcessing as DP


def utility(pattern):
    """
    :param pattern: 输入的需要计算的模式例如：[["1002", "1003"]["1004"]]
    :return: 返回模式pattern的效用�?�u(pattern)
    """
    utilityValue = 0
    for itemSets in pattern:
        for item in itemSets:
            utilityValue += utilityTable[item]
    return utilityValue


def sc(patternPosition):
    """
    计算支持�?

    :param patternPosition: 模式pattern的出现位置纪�?
    :return: 返回该模式的支持�?
    """
    supportValue = 0
    for sequenceId in patternPosition.keys():
        supportValue += len(patternPosition[sequenceId][0])
    return supportValue


def lenPattern(pattern):
    """
    计算模式pattern长度 ：pattern中项的个�?

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


def auCalculate(pattern, patternPosition):
    """
    计算模式pattern的平均效�?

    :param patternPosition: 模式pattern的出现位置纪�?
    :param pattern: 模式pattern
    :return: 模式pattern的平均效�?
    """
    supportValue = sc(patternPosition)
    utilityValue = utility(pattern)
    length = lenPattern(pattern)
    averageUtility = (supportValue * utilityValue) / length
    return averageUtility


def mtb(pattern, patternPosition):
    """

    :param
    allItemList:按照元素效用值排�?
    :return:fnd[i]
    """
    uv = utility(pattern)
    auv = uv / lenPattern(pattern)
    maxs = 0
    num = 0
    for sequenceId in patternPosition.keys():
        endIndex = patternPosition[sequenceId][-1][0]
        i = 0
        value = 0
        indexs = 0
        while allItemList[1][i] > auv:
            index = 0
            if sequenceId in dataTable[allItemList[0][i]].keys():
                for j in dataTable[allItemList[0][i]][sequenceId][0]:
                    if j > endIndex:
                        index += 1
                uvi = index * allItemList[1][i]
                value += uvi
            i += 1
            indexs += index

            if i == len(allItemList[0]):
                break
        if maxs < value:
            maxs = value
            num = indexs
    allu = uv + maxs
    mtbv = sc(patternPosition) * allu / (lenPattern(pattern) + num)

    return mtbv


def saveTopkPattern(pattern, au, minau):
    """

    :type listsTemp: list
    :param listsTemp:
    :param pattern:
    :param au:
    :param minau:
    :return:
    """
    lengthOfList = len(listsTemp[0])
    if lengthOfList < kValue:
        indexTemp = 0
        while indexTemp < lengthOfList and listsTemp[1][indexTemp] > au:
            indexTemp += 1
        listsTemp[0].insert(indexTemp, pattern)
        listsTemp[1].insert(indexTemp, au)
        if lengthOfList + 1 == kValue:
            minau = listsTemp[1][kValue - 1]

    else:
        indexTemp = 0
        while indexTemp < lengthOfList and listsTemp[1][indexTemp] > au:
            indexTemp += 1
        if indexTemp <= lengthOfList:
            listsTemp[0].insert(indexTemp, pattern)
            listsTemp[1].insert(indexTemp, au)
            listsTemp[0].pop()
            listsTemp[1].pop()
        minau = listsTemp[1][kValue - 1]

    return minau


def oneOff(itemSetExitInter, newPatternPosition, newpatternAllPosition):
    """
    �?次�?�判�?
    满足�?次�?�返回True，否则返回False

    :param itemSetExitInter:序列模式中各项集之间的交集关�?
    :param newPatternPosition:
    :param newpatternAllPosition:
    :return:
    """
    for patternIndex in itemSetExitInter:
        if newpatternAllPosition[0] in newPatternPosition[patternIndex]:
            return False
    return True


def inter(seta, setb):
    """
    返回seta和setb的交�?

    :param seta:
    :param setb:
    :return:
    """
    return list(set(seta) & set(setb))


def twoToMore(L2, flag, minau):
    L3 = []

    return L3, flag, minau


def OSC(position1, deletePosition1, position2, deletePosition2):
    newPatternPosition = {}
    newPatternDeletePosition = {}
    return newPatternPosition, newPatternDeletePosition


def oneToTwo(L1, minau):
    global candidatePatternNum
    len1 = len(L1)
    L2 = []
    for i in range(0, len1):
        if L1[i][3] > minau:
            p1 = L1[i][0]
            position1 = L1[i][2]
            deletePosition1 = L1[i][4]
            for j in range(0, len1):
                if L1[j][3] > minau:
                    p2 = L1[j][0]
                    position2 = L1[j][2]
                    deletePosition2 = L1[j][4]
                     # 相等的时候，�?种情�?(a)(b); (a)(a),直接拼接
                    newPattern = [p1[0], p2[0]]
                    candidatePatternNum += 1
                    newPatternPosition, newPatternDeletePosition= OSC(position1, deletePosition1, position2, deletePosition2)
                    sup = sc(newPatternPosition)
                    au = auCalculate(newPattern, newPatternPosition)
                    msub = mtb(newPattern, newPatternPosition)
                    if msub > minau:
                        if au > minau:
                            minau = saveTopkPattern(newPattern, au, minau)
                        L2.append([newPattern, newPatternPosition, msub, newPatternDeletePosition])
                    if i > j:  # 不相等的时�?�，存在相集扩展
                        p3 = [[p1[0][0],p1[0][0]]]
                        candidatePatternNum += 1
                        newPatternPosition, newPatternDeletePosition = OSC(position1, deletePosition1, position2, deletePosition2)
                        sup = sc(newPatternPosition)
                        au = auCalculate(newPattern, newPatternPosition)
                        msub = mtb(newPattern, newPatternPosition)
                        if msub > minau:
                            if au > minau:
                                minau = saveTopkPattern(newPattern, au, minau)
                            L2.append([newPattern, newPatternPosition, msub, newPatternDeletePosition])
    return L2, minau


def HATKMAIN():
    """

    :return:
    """
    global allItemList, candidatePatternNum, listsTemp
    L = []
    minau = 0
    # 生成1-长度的序�?
    for item in utilityTable.keys():
        u = utilityTable[item]
        allItemList[0].append(item)
        allItemList[1].append(u)
    for item in utilityTable.keys():
        candidatePatternNum += 1
        deletePosition = {}
        position = {}
        for dt in dataTable[item]:
            position[dt] = dataTable[item][dt]
            deletePosition[dt] = [[]]
        au = auCalculate([[item]], position)
        msub = mtb([[item]], position)
        if msub > minau:
            if au > minau:
                minau = saveTopkPattern([[item]], au, minau)
            L.append([[[item]], list(utilityTable.keys()).index(item) + 1, position, msub, deletePosition])
    L, minau = oneToTwo(L, minau)
    flag = 1
    while flag:
        L, flag, minau = twoToMore(L, flag, minau)


if __name__ == '__main__':
    # fn = [['../Data/chainstoreUtility.txt', '../Data/chainstore.txt'],
    #       ['../Data/MicroblogPCUUtility.txt', '../Data/MicroblogPCU.txt'],
    #       ['../Data/OnlineRetail2DatasetUtility.txt', '../Data/OnlineRetail2Dataset.txt'],
    #       ['../Data/OnlineRetail1Dataset.txt', '../Data/OnlineRetail1DatasetUtility.txt'],
    #       ['../Data/Sds1-utility.txt', '../Data/Sds1.txt'],
    #       ['../Data/Sds2-utility.txt', '../Data/Sds2.txt'],
    #       ['../Data/Sds3-utility.txt', '../Data/Sds3.txt'],
    #       ['../Data/DS10L1S6L8I5000F-utility.txt', '../Data/DS10L1S6L8I5000F.txt'],
    #       ['../Data/creatDataUtility1.txt', '../Data/creatData1.txt'],
    #       ['../Data/creatData2Utility.txt', '../Data/creatData2.txt'],
    #       ['../Data/creatData3Utility.txt', '../Data/creatData3.txt'],
    #       ['../Data/creatDataUtility4.txt', '../Data/creatData4.txt']]
    # kL = [10, 50, 100, 200, 500, 1000, 1500, 2000, 25000, 3000]
    # kValue = 1
    # for kValue in kL:
    #     for i in range(0, len(fn)):
    #         utilityTable = DP.operateUtilityTableFile1(fn[i][0])
    #         dataTable = DP.operateDataFile1(utilityTable, fn[i][1])
    #         listsTemp = [[], []]
    #         allItemList = [[], []]
    #         candidatePatternNum = 0
    #         starTime = time.time()
    #         maxs = memory_usage(HATKMAIN, max_usage=True)
    #         endTime = time.time()
    #         print("k = " + str(kValue) + ", " + fn[i][1])
    #         with open("../Result/TOAP-noorder-result.txt", 'a') as f:
    #             f.write("\n----------------------------------------------------------------------\n")
    #             f.write("k = " + str(kValue) + ", " + fn[i][1] + "\n")
    #             f.write("�?大内存使用：" + str(maxs) + "Mb" + "\n")
    #             f.write("运行时间�?" + str(endTime * 1000 - starTime * 1000) + "ms" + "\n")
    #             f.write("候�?�模式数量：" + str(candidatePatternNum) + "\n")
    #             f.write(str(listsTemp))

    #
    # # utilityTable = {"a": 6, "b": 1, "c": 5, "d": 2, "e": 4, "f": 3}
    # # dataTable = {"a": {"1": [[1, 2, 3]], "2": [[1, 2]], "3": [[2, 3]], "4": [[1, 4]], "5": [[2]]},
    # #              "b": {"1": [[2, 3]], "2": [[2, 3]], "3": [[2, 3]], "4": [[2]], "5": [[1, 3]]},
    # #              "c": {"1": [[1, 2, 5]], "2": [[3]], "4": [[3, 4]], "5": [[3, 5]]},
    # #              "d": {"1": [[3]], "2": [[2, 3]], "3": [[3]], "4": [[3]], "5": [[2, 5]]},
    # #              "e": {"1": [[4]], "2": [[1, 3]], "4": [[2]], "5": [[1, 2, 3]]},
    # #              "f": {"1": [[5]], "3": [[1]], "5": [[4]]}}
    utilityTable = {"a": 2.1, "b": 1.2}
    dataTable = {"a": {"1": [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]]}, "b": {"1": [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]]}}
    # # utilityTable = {"a": 10, "b": 5, "c": 8, "d": 3}
    # # dataTable = {"a": {"1": [[1, 2, 3, 5, 6]], "2": [[1, 2, 3, 5, 7]], "3": [[1, 2, 3]], "4": [[1, 2, 4, 6]]},
    # #              "b": {"1": [[1, 2, 4, 5]], "2": [[2, 3, 5, 8]], "3": [[2, 3, 5, 6]], "4": [[2]]},
    # #              "c": {"2": [[2, 4, 5, 7]], "4": [[3, 4, 6]]},
    # #              "d": {"1": [[4]], "2": [[2, 4, 6, 8]], "3": [[1, 3, 4, 6]], "4": [[1, 2, 3, 5, 7]]}
    # #              }
    kValue = 10
    cPIL = []
    listsTemp = [[], []]
    allItemList = [[], []]
    allUList = [[], []]
    candidatePatternNum = 0
    starTime = time.time()
    maxs = memory_usage((HATKMAIN), max_usage=True)
    # Lists = HATKMAIN()
    endTime = time.time()
    # print("k = " + str(kValue) + ", " + fnd[i])
    print("�?大内存使用：" + str(maxs) + "Mb")
    print("运行时间�?" + str(endTime * 1000 - starTime * 1000) + "ms")
    print("候�?�模式数量：" + str(candidatePatternNum))
    print(str(listsTemp))
# ��������
