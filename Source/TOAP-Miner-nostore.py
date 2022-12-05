import time
#
# from memory_profiler import memory_usage

from Tool import DataProcessing as DP


def utility(p):
    """
    :param p: 输入的需要计算的模式例如：[["1002", "1003"]["1004"]]
    :return: 返回模式pattern的效用值u(pattern)
    """
    uv = 0
    for i in p:
        for it in i:
            uv += utilityTable[it]
    return uv


def sc(pp):
    """
    计算支持度

    :param pp: 模式pattern的出现位置纪录
    :return: 返回该模式的支持度
    """
    sv = 0
    for si in pp.keys():
        sv += len(pp[si][0])
    return sv


def lenPattern(p):
    """
    计算模式pattern长度 ：pattern中项的个数

    :param pattern: 模式pattern
    :return: 模式pattern的长度：各项集中项数之和
    """
    l = 0
    for i in p:
        l += len(i)
    return l


def sizePattern(p):
    """

    :param p: 模式pattern
    :return: 模式pattern的大小：项集个数
    """
    return len(p)


def auCalculate(p, pp):
    """
    计算模式pattern的平均效用

    :param pp: 模式pattern的出现位置纪录
    :param p: 模式pattern
    :return: 模式pattern的平均效用
    """
    sv = sc(pp)
    u = utility(p)
    l = lenPattern(p)
    au = sv * u / l
    return au


def saveTopkPattern(pattern, ListsTemp, au, minau):
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

    return minau


def mtb(pattern, patternPosition):
    """

    :param
    allItemList:按照元素效用值排序
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
        while allUList[1][i] > auv:
            index = 0
            if sequenceId in dataTable[allUList[0][i]].keys():
                for j in dataTable[allUList[0][i]][sequenceId][0]:
                    if j > endIndex:
                        index += 1
                uvi = index * allUList[1][i]
                value += uvi
            i += 1
            indexs += index
        if maxs < value:
            maxs = value
            num = indexs
    allu = uv + maxs
    mtbv = sc(patternPosition) * allu / (lenPattern(pattern) + num)

    return mtbv


def oneOff1(itemset, i, R):
    for p in itemset:
        if i[0] in R[p]:
            return False
    return True



def inter(seta, setb):
    """
    返回seta和setb的交集

    :param seta:
    :param setb:
    :return:
    """
    return sorted(list(set(seta) & set(setb)))


def eP(minau):
    """
    模式增长

    :param ListsTemp: top-k个模式及其平均效用值
    :param minau: 最小支持度阈值
    :return:
    """
    global candidatePatternNum
    patternInfor = cPIL[0]
    sizeOfPattern = len(patternInfor[0])

    # 序列扩展
    for item in allItemList[0]:
        index = allItemList[0].index(item)
        if allItemList[1][index] > minau:
            # 得到newPattern
            candidatePatternNum += 1
            newPattern = patternInfor[0][:]
            newPattern.append([item])
            R = {}
            newPatternAllPosition = {}
            si = list(dataTable[item].keys())[:]
            for itemset in newPattern:
                for items in itemset:
                    R[items] = []
                    si = inter(si, list(dataTable[items])[:])
            for id in si:
                newPatternAllPosition[id] = []
                for itemset in newPattern:
                    isl = []
                    for items in itemset:
                        if isl:
                            isl = inter(isl, dataTable[items][id][0][:])
                        else:
                            isl = dataTable[items][id][0][:]
                    newPatternAllPosition[id].append(isl)
            newPatternPosition = {}
            for pi in newPatternAllPosition:
                for item in R.keys():
                    R[item] = []
                newPatternPosition[pi] = []
                flagWhile = 1
                while flagWhile and newPatternAllPosition[pi][0]:
                    occurrencePosition = []

                    # 对每个序列的第一个项集进行查找可以使用的位置
                    i = 0
                    while flagWhile and newPatternPosition[pi] and not oneOff1(newPattern[i], newPatternAllPosition[pi][i], R):
                        newPatternAllPosition[pi][i].pop(0)
                        if not newPatternAllPosition[pi][i]:
                            # 若第一个项集没有可扩展的位置时，flagWhile = 0
                            flagWhile = 0
                    if flagWhile:
                        occurrencePosition.append([newPatternAllPosition[pi][i][0]])
                        newPatternAllPosition[pi][i].pop(0)
                        i += 1
                    # 对第二个项集及以后的项集进行选择 满足一次性的位置
                    while flagWhile and i < sizeOfPattern + 1:
                        if newPatternAllPosition[pi][i]:
                            if newPatternPosition[pi]:
                                while flagWhile and (
                                        newPatternAllPosition[pi][i][0] <= occurrencePosition[i - 1][0] or not oneOff1(newPattern[i], newPatternAllPosition[pi][i], R)):
                                    newPatternAllPosition[pi][i].pop(0)
                                    if not newPatternAllPosition[pi][i]:
                                        # 若第i+1个项集没有可扩展的位置时，flagWhile = 0
                                        flagWhile = 0
                            else:
                                while flagWhile and newPatternAllPosition[pi][i][0] <= occurrencePosition[i - 1][0]:
                                    newPatternAllPosition[pi][i].pop(0)
                                    if not newPatternAllPosition[pi][i]:
                                        # 若第i+1个项集没有可扩展的位置时，flagWhile = 0
                                        flagWhile = 0
                        else:
                            # 若第i+1个项集没有可扩展的位置时，flagWhile = 0
                            flagWhile = 0
                        if flagWhile:
                            # flagWhile=1，本次循环产生完整的模式出现位置，将其记录在occurrencePosition中
                            occurrencePosition.append([newPatternAllPosition[pi][i][0]])
                            newPatternAllPosition[pi][i].pop(0)
                            i += 1
                    if flagWhile:
                        # flagWhile = 1，走到这一步说明新模式在序列patternIndex中有一个完整的出现生成，并将其存入newPatternPosition[pi]中
                        for id in range(0, len(newPattern)):
                            for item in newPattern[id]:
                                R[item].append(occurrencePosition[id][0])
                        if not newPatternPosition[pi]:
                            newPatternPosition[pi] = occurrencePosition
                        else:
                            for j in range(0, sizeOfPattern + 1):
                                newPatternPosition[pi][j] = newPatternPosition[pi][j] + \
                                                            occurrencePosition[j]

                if not newPatternPosition[pi]:
                    newPatternPosition.pop(pi)
                elif not newPatternPosition[pi][0]:
                    newPatternPosition.pop(pi)
            au = auCalculate(newPattern, newPatternPosition)
            msub = mtb(newPattern, newPatternPosition)
            if msub > minau:
                if au > minau:
                    minau = saveTopkPattern(newPattern, ListsTemp, au, minau)
                cPIL.append([newPattern, index + 1, msub])
        else:
            break
    # 项集扩展
    for item in allItemList[0][patternInfor[1]:]:
        index = allItemList[0].index(item)
        if allItemList[1][index] > minau:
            # 得到newPattern
            candidatePatternNum += 1
            newPattern = patternInfor[0][:sizeOfPattern - 1]
            newPattern.append(patternInfor[0][sizeOfPattern - 1][:])
            newPattern[sizeOfPattern - 1].append(item)

            R = {}
            # 初始化
            """
            纪录新模式中各项集之间是否有相同项
            """
            # 可优化:纪录上一个模式的itemSetExitInter集合，只需对增加的项集进行查找是否有相同的项即可
            itemSetExitInter = []
            for i in range(0, sizeOfPattern):
                itemSetExitInter.append([])
            for i in range(0, sizeOfPattern):
                for j in range(i + 1, sizeOfPattern):
                    if inter(newPattern[i], newPattern[j]):
                        itemSetExitInter[i].append(j)
                        itemSetExitInter[j].append(i)
            newPatternAllPosition = {}
            si = list(dataTable[item].keys())[:]
            for itemset in newPattern:
                for items in itemset:
                    R[items] = []
                    si = inter(si, list(dataTable[items])[:])
            for id in si:
                newPatternAllPosition[id] = []
                for itemset in newPattern:
                    isl = []
                    for items in itemset:
                        if isl:
                            isl = inter(isl, dataTable[items][id][0][:])
                            if isl == []:
                                break
                        else:
                            isl = dataTable[items][id][0][:]
                    newPatternAllPosition[id].append(isl)
            newPatternPosition = {}
            for pi in newPatternAllPosition:
                for item in R.keys():
                    R[item] = []
                newPatternPosition[pi] = []
                flagWhile = 1
                while flagWhile and newPatternAllPosition[pi][0]:
                    occurrencePosition = []

                    # 对每个序列的第一个项集进行查找可以使用的位置
                    i = 0
                    while flagWhile and newPatternPosition[pi] and not oneOff1(newPattern[i], newPatternAllPosition[pi][i], R):
                        newPatternAllPosition[pi][i].pop(0)
                        if not newPatternAllPosition[pi][i]:
                            # 若第一个项集没有可扩展的位置时，flagWhile = 0
                            flagWhile = 0
                    if flagWhile:
                        occurrencePosition.append([newPatternAllPosition[pi][i][0]])
                        newPatternAllPosition[pi][i].pop(0)
                        i += 1
                    # 对第二个项集及以后的项集进行选择 满足一次性的位置
                    while flagWhile and i < sizeOfPattern:
                        if newPatternAllPosition[pi][i]:
                            if newPatternPosition[pi]:
                                while flagWhile and (newPatternAllPosition[pi][i][0] <= occurrencePosition[i - 1][0] or not oneOff1(newPattern[i], newPatternAllPosition[pi][i], R)):
                                    newPatternAllPosition[pi][i].pop(0)
                                    if not newPatternAllPosition[pi][i]:
                                        # 若第i+1个项集没有可扩展的位置时，flagWhile = 0
                                        flagWhile = 0
                            else:
                                while flagWhile and newPatternAllPosition[pi][i][0] <= occurrencePosition[i - 1][0]:
                                    newPatternAllPosition[pi][i].pop(0)
                                    if not newPatternAllPosition[pi][i]:
                                        # 若第i+1个项集没有可扩展的位置时，flagWhile = 0
                                        flagWhile = 0
                        else:
                            # 若第i+1个项集没有可扩展的位置时，flagWhile = 0
                            flagWhile = 0
                        if flagWhile:
                            # flagWhile=1，本次循环产生完整的模式出现位置，将其记录在occurrencePosition中
                            occurrencePosition.append([newPatternAllPosition[pi][i][0]])
                            newPatternAllPosition[pi][i].pop(0)
                            i += 1
                    if flagWhile:
                        # flagWhile = 1，走到这一步说明新模式在序列patternIndex中有一个完整的出现生成，并将其存入newPatternPosition[pi]中
                        for id in range(0, len(newPattern)):
                            for item in newPattern[id]:
                                R[item].append(occurrencePosition[id][0])
                        if not newPatternPosition[pi]:
                            newPatternPosition[pi] = occurrencePosition
                        else:
                            for j in range(0, sizeOfPattern):
                                newPatternPosition[pi][j] = newPatternPosition[pi][j] + \
                                                            occurrencePosition[j]
                if not newPatternPosition[pi]:
                    newPatternPosition.pop(pi)
                elif not newPatternPosition[pi][0]:
                    newPatternPosition.pop(pi)
            au = auCalculate(newPattern, newPatternPosition)
            msub = mtb(newPattern, newPatternPosition)
            if msub > minau:
                if au > minau:
                    minau = saveTopkPattern(newPattern, ListsTemp, au, minau)
                cPIL.append([newPattern, index + 1, msub])
        else:
            break
    return minau


def HATKMAIN():
    # 保存高平均效用模式
    # 初始化变量
    global candidatePatternNum, ListsTemp
    minau = 0
    for item in utilityTable.keys():
        length = len(allUList[0])
        index = 0
        au = utilityTable[item]
        while length > index and allUList[1][index] >= au:
            index = index + 1
        allUList[0].insert(index, item)
        allUList[1].insert(index, au)

    for item in utilityTable.keys():
        position = dataTable[item]
        pattern = [[item]]
        msub = mtb(pattern, position)
        length = len(allItemList[0])
        index = 0
        while length > index and allItemList[1][index] >= msub:
            index = index + 1
        allItemList[0].insert(index, item)
        allItemList[1].insert(index, msub)
    # 生成1-长度的序列
    for item in allItemList[0]:
        candidatePatternNum += 1
        index = allItemList[0].index(item)
        msub = allItemList[1][index]
        if msub > minau:
            position = {}
            for dt in dataTable[item]:
                position[dt] = dataTable[item][dt]
            au = auCalculate([[item]], position)
            if au > minau:
                minau = saveTopkPattern([[item]], ListsTemp, au, minau)
            cPIL.append([[[item]], index + 1, msub])
    # 模式增长，
    while cPIL:
        msub = cPIL[0][2]
        if msub > minau:
            minau = eP(minau)
        cPIL.pop(0)


if __name__ == '__main__':
    # # 数据库预处理
    fn = [['../Data/chainstoreUtility.txt', '../Data/chainstore.txt'],
          ['../Data/OnlineRetail2DatasetUtility.txt', '../Data/OnlineRetail2Dataset.txt'],
          ['../Data/OnlineRetail1Dataset.txt', '../Data/OnlineRetail1DatasetUtility.txt'],
          ['../Data/DS10L1S6L8I5000F-utility.txt', '../Data/DS10L1S6L8I5000F.txt'],
          ['../Data/creatData2Utility.txt', '../Data/creatData2.txt'],
          ['../Data/creatData3Utility.txt', '../Data/creatData3.txt'],
          ['../Data/E-ShopUtility.txt', '../Data/E-Shop.txt'],
          ['../Data/SignUtility.txt', '../Data/Sign.txt']]
    # fn = [['../Data/example/3Utility.txt', '../Data/example/3.txt']]
    kL = [10, 50, 100, 200, 500, 1000, 1500, 2000, 25000, 3000]
    # kL = [8]
    kValue = 0
    for kValue in kL:
        for i in range(0, len(fn)):
            utilityTable = DP.operateUtilityTableFile1(fn[i][0])
            dataTable = DP.operateDataFile1(utilityTable, fn[i][1])
            cPIL = []
            ListsTemp = [[], []]
            allItemList = [[], []]
            allUList = [[], []]
            candidatePatternNum = 0
            starTime = time.time()
            # maxs = memory_usage((HATKMAIN), max_usage=True)
            HATKMAIN()
            endTime = time.time()
            print("k = " + str(kValue) + ", " + fn[i][1])
            with open("../Result/TOAP-nostore-result.txt", 'a') as f:
                f.write("\n----------------------------------------------------------------------\n")
                f.write("k = " + str(kValue) + ", " + fn[i][1] + "\n")
                # f.write("最大内存使用：" + str(maxs) + "Mb" + "\n")
                f.write("运行时间：" + str(endTime * 1000 - starTime * 1000) + "ms" + "\n")
                f.write("候选模式数量：" + str(candidatePatternNum) + "\n")
                f.write(str(ListsTemp))
    # 小型例子
    # utilityTable = {"a": 6, "b": 1, "c": 5, "d": 2, "e": 4, "f": 3}
    # dataTable = {"a": {"1": [[1, 2, 3]], "2": [[1, 2]], "3": [[2, 3]], "4": [[1, 4]], "5": [[2]]},
    #              "b": {"1": [[2, 3]], "2": [[2, 3]], "3": [[2, 3]], "4": [[2]], "5": [[1, 3]]},
    #              "c": {"1": [[1, 2, 5]], "2": [[3]], "4": [[3, 4]], "5": [[3, 5]]},
    #              "d": {"1": [[3]], "2": [[2, 3]], "3": [[3]], "4": [[3]], "5": [[2, 5]]},
    #              "e": {"1": [[4]], "2": [[1, 3]], "4": [[2]], "5": [[1, 2, 3]]},
    #              "f": {"1": [[5]], "3": [[1]], "5": [[4]]}}
    # utilityTable = {"a": 2.1, "b": 1.2}
    # dataTable = {"a": {"1": [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]]}, "b": {"1": [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]]}}
    # utilityTable = {"a": 10, "b": 5, "c": 8, "d": 3}
    # dataTable = {"a": {"1": [[1, 3, 4, 5, 6]], "2": [[1, 2, 3, 4, 6]]},
    #              "b": {"1": [[1, 3, 4, 6]], "2": [[2, 3, 4]]},
    #              "c": {"1": [[2, 3, 4, 5]], "2": [[1, 3, 5, 6]]},
    #              "d": {"1": [[5]], "2": [[3, 5]]}
    #              }
    # kValue = 8
    # cPIL = []
    # allItemList = [[], []]
    # allUList = [[], []]
    # ListsTemp = [[], []]
    # candidatePatternNum = 0
    # starTime = time.time()
    # # maxs = memory_usage((HATKMAIN), max_usage=True)
    # HATKMAIN()
    # endTime = time.time()
    # # print("k = " + str(kValue) + ", " + fnd[i])
    # # print("最大内存使用：" + str(maxs) + "Mb")
    # print(ListsTemp)
    # print("运行时间：" + str(endTime * 1000 - starTime * 1000) + "ms")
    # print("候选模式数量：" + str(candidatePatternNum))

