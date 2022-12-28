import time

# from memory_profiler import memory_usage

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


def sc(patternPosition):
    """
    计算支持度

    :param patternPosition: 模式pattern的出现位置纪录
    :return: 返回该模式的支持度
    """
    supportValue = 0
    for sequenceId in patternPosition.keys():
        supportValue += len(patternPosition[sequenceId][0])
    return supportValue


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


def auCalculate(pattern, patternPosition):
    """
    计算模式pattern的平均效用

    :param patternPosition: 模式pattern的出现位置纪录
    :param pattern: 模式pattern
    :return: 模式pattern的平均效用
    """
    supportValue = sc(patternPosition)
    utilityValue = utility(pattern)
    length = lenPattern(pattern)
    averageUtility = (supportValue * utilityValue) / length
    return averageUtility


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


def oneOff(itemSetExitInter, newPatternPosition, newpatternAllPosition):
    """
    一次性判断
    满足一次性返回True，否则返回False

    :param itemSetExitInter:序列模式中各项集之间的交集关系
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
    返回seta和setb的交集

    :param seta:
    :param setb:
    :return:
    """
    return list(set(seta) & set(setb))


def EP(ListsTemp, minau):
    """
    模式增长

    :param ListsTemp: top-k个模式及其平均效用值
    :param minau: 最小支持度阈值
    :return:
    """
    global candidatePatternNum
    patternInfor = cPIL[0]
    sizeOfPattern = len(patternInfor[0])
    oldPatternPosition = patternInfor[2]
    oldPatternDeletePosition = patternInfor[4]

    # 序列扩展
    for item in allItemList[0]:
        index = allItemList[0].index(item)
        # 得到newPattern
        newPattern = patternInfor[0][:]
        newPattern.append([item])
        candidatePatternNum += 1
        # 初始化
        newPatternPosition = {}
        newPatternDeletePosition = {}
        itemPosition = dataTable[item]
        """
        纪录新模式中各项集之间是否有相同项
        """
        # 可优化:纪录上一个模式的itemSetExitInter集合，只需对增加的项集进行查找是否有相同的项即可
        # 时间优化，占用空间
        itemSetExitInter = []
        for i in range(0, sizeOfPattern + 1):
            itemSetExitInter.append([])
        for i in range(0, sizeOfPattern + 1):
            for j in range(i + 1, sizeOfPattern + 1):
                if inter(newPattern[i], newPattern[j]):
                    itemSetExitInter[i].append(j)
                    itemSetExitInter[j].append(i)
        """进行计算新模式的位置信息"""
        for patternIndex in oldPatternPosition.keys():
            '''
                此循环使得patternIndex遍历包含oldPattern的序列号
                if语句确保oldPattern和itme出现在同一个序列中
            '''
            if patternIndex in itemPosition.keys():  # 确保pattern和新增加的元素在同一个序列中出现
                newPatternPosition[patternIndex] = []
                newPatternDeletePosition[patternIndex] = []
                for i in range(0, sizeOfPattern + 1):
                    newPatternDeletePosition[patternIndex].append([])
                # 生成新模式中各项集出现的所有位置集合
                newpatternAllPosition = []
                for itemSetNum in range(0, sizeOfPattern):
                    newpatternAllPosition.append(
                        oldPatternPosition[patternIndex][:][itemSetNum][:] + oldPatternDeletePosition[patternIndex][:][
                                                                                 itemSetNum][:])
                newpatternAllPosition.append(itemPosition[patternIndex][0][:])

                flagWhile = 1
                while flagWhile and newpatternAllPosition[0]:
                    occurrencePosition = []

                    # 对每个序列的第一个项集进行查找可以使用的位置
                    i = 0
                    while flagWhile and newPatternPosition[patternIndex] and not oneOff(itemSetExitInter[i],
                                                                                        newPatternPosition[
                                                                                            patternIndex],
                                                                                        newpatternAllPosition[i]):
                        newPatternDeletePosition[patternIndex][i].append(newpatternAllPosition[i][0])
                        newpatternAllPosition[i].pop(0)
                        if not newpatternAllPosition[i]:
                            # 若第一个项集没有可扩展的位置时，flagWhile = 0
                            flagWhile = 0
                    if flagWhile:
                        occurrencePosition.append([newpatternAllPosition[i][0]])
                        newpatternAllPosition[i].pop(0)
                        i += 1

                    # 对第二个项集及以后的项集进行选择 满足一次性的位置
                    while flagWhile and i < sizeOfPattern + 1:
                        if newpatternAllPosition[i]:
                            if newPatternPosition[patternIndex]:
                                while flagWhile and (
                                        newpatternAllPosition[i][0] <= occurrencePosition[i - 1][0] or not oneOff(
                                    itemSetExitInter[i], newPatternPosition[patternIndex],
                                    newpatternAllPosition[i])):
                                    newPatternDeletePosition[patternIndex][i].append(newpatternAllPosition[i][0])
                                    newpatternAllPosition[i].pop(0)
                                    if not newpatternAllPosition[i]:
                                        # 若第i+1个项集没有可扩展的位置时，flagWhile = 0
                                        flagWhile = 0
                            else:
                                while flagWhile and newpatternAllPosition[i][0] <= occurrencePosition[i - 1][0]:
                                    newPatternDeletePosition[patternIndex][i].append(newpatternAllPosition[i][0])
                                    newpatternAllPosition[i].pop(0)
                                    if not newpatternAllPosition[i]:
                                        # 若第i+1个项集没有可扩展的位置时，flagWhile = 0
                                        flagWhile = 0
                        else:
                            # 若第i+1个项集没有可扩展的位置时，flagWhile = 0
                            flagWhile = 0
                        if flagWhile:
                            # flagWhile=1，本次循环产生完整的模式出现位置，将其记录在occurrencePosition中
                            occurrencePosition.append([newpatternAllPosition[i][0]])
                            newpatternAllPosition[i].pop(0)
                            i += 1
                    if flagWhile:
                        # flagWhile = 1，走到这一步说明新模式在序列patternIndex中有一个完整的出现生成，并将其存入newPatternPosition[patternIndex]中
                        if not newPatternPosition[patternIndex]:
                            newPatternPosition[patternIndex] = occurrencePosition
                        else:
                            for j in range(0, sizeOfPattern + 1):
                                newPatternPosition[patternIndex][j] = newPatternPosition[patternIndex][j] + \
                                                                      occurrencePosition[j]
                    else:
                        # flagWhile = 0 表示生成完成一次性出现挖掘的过程未挖掘出完整的出现，此时需要将occurrencePosition和newpatternAllPosition
                        # 中的位置存入newPatternDeletePosition[patternIndex]中
                        for itemSetNum in range(0, sizeOfPattern + 1):
                            if itemSetNum < len(occurrencePosition):
                                newPatternDeletePosition[patternIndex][itemSetNum] += newpatternAllPosition[
                                                                                          itemSetNum] + \
                                                                                      occurrencePosition[itemSetNum]
                            else:
                                newPatternDeletePosition[patternIndex][itemSetNum] += newpatternAllPosition[
                                    itemSetNum]
                for itemsIndex in range(0, sizePattern(newPattern)):
                    if newpatternAllPosition[itemsIndex]:
                        newPatternDeletePosition[patternIndex][itemsIndex] = sorted(list(
                            set(newpatternAllPosition[itemsIndex]).union(
                                set(newPatternDeletePosition[patternIndex][itemsIndex]))))
                if not newPatternPosition[patternIndex]:
                    newPatternPosition.pop(patternIndex)
                    newPatternDeletePosition.pop(patternIndex)
                elif not newPatternPosition[patternIndex][0]:
                    newPatternPosition.pop(patternIndex)
                    newPatternDeletePosition.pop(patternIndex)
        au = auCalculate(newPattern, newPatternPosition)
        msub = mtb(newPattern, newPatternPosition)
        if msub > minau:
            if au > minau:
                minau = saveTopkPattern(newPattern, ListsTemp, au, minau)
            cPIL.append([newPattern, index + 1, newPatternPosition, msub, newPatternDeletePosition])

    # 项集扩展
    for item in allItemList[0][patternInfor[1]:]:
        index = allItemList[0].index(item)

        # 得到newPattern
        newPattern = patternInfor[0][:sizeOfPattern - 1]
        newPattern.append(patternInfor[0][sizeOfPattern - 1][:])
        newPattern[sizeOfPattern - 1].append(item)
        candidatePatternNum += 1
        newPatternPosition = {}
        newPatternDeletePosition = {}
        itemPosition = dataTable[item]

        # 可优化，同4
        itemSetExitInter = []
        for i in range(0, sizeOfPattern):
            itemSetExitInter.append([])
        for i in range(0, sizeOfPattern):
            for j in range(i + 1, sizeOfPattern):
                if inter(newPattern[i], newPattern[j]):
                    itemSetExitInter[i].append(j)
                    itemSetExitInter[j].append(i)
        for patternIndex in oldPatternPosition.keys():
            if patternIndex in itemPosition.keys():
                newPatternPosition[patternIndex] = []
                newPatternDeletePosition[patternIndex] = []
                for i in range(0, sizeOfPattern):
                    newPatternDeletePosition[patternIndex].append([])
                # 生成新模式中各项集出现的所有位置集合
                newpatternAllPosition = []
                for itemSetNum in range(0, sizeOfPattern):
                    newpatternAllPosition.append(oldPatternPosition[patternIndex][:][itemSetNum][:] +
                                                 oldPatternDeletePosition[patternIndex][:][itemSetNum][:])
                newpatternAllPosition[sizeOfPattern - 1] = inter(newpatternAllPosition[sizeOfPattern - 1][:],
                                                                 itemPosition[patternIndex][:][0][:])
                flagWhile = 1
                while flagWhile and newpatternAllPosition[0]:
                    # 每一次循环都会产一次，或者跳出循环
                    occurrencePosition = []
                    # 对每个序列的第一个项集进行查找对的位置
                    i = 0
                    while flagWhile and newPatternPosition[patternIndex] and not oneOff(itemSetExitInter[i],
                                                                                        newPatternPosition[
                                                                                            patternIndex],
                                                                                        newpatternAllPosition[i]):
                        newPatternDeletePosition[patternIndex][i].append(newpatternAllPosition[i][0])
                        newpatternAllPosition[i].pop(0)
                        if not newpatternAllPosition[i]:
                            flagWhile = 0
                    if flagWhile:
                        occurrencePosition.append([newpatternAllPosition[i][0]])
                        newpatternAllPosition[i].pop(0)
                        i += 1
                    # 对第二个项集及以后的项集进行选择满足一次性的位置
                    while flagWhile and i < sizeOfPattern:
                        if newpatternAllPosition[i]:
                            if newPatternPosition[patternIndex]:
                                while flagWhile and (
                                        newpatternAllPosition[i][0] <= occurrencePosition[i - 1][0] or not oneOff(
                                    itemSetExitInter[i], newPatternPosition[patternIndex],
                                    newpatternAllPosition[i])):
                                    newPatternDeletePosition[patternIndex][i].append(newpatternAllPosition[i][0])
                                    newpatternAllPosition[i].pop(0)
                                    if not newpatternAllPosition[i]:
                                        flagWhile = 0
                            else:
                                while flagWhile and newpatternAllPosition[i][0] <= occurrencePosition[i - 1][0]:
                                    newPatternDeletePosition[patternIndex][i].append(newpatternAllPosition[i][0])
                                    newpatternAllPosition[i].pop(0)
                                    if not newpatternAllPosition[i]:
                                        flagWhile = 0
                        else:
                            flagWhile = 0
                        if flagWhile:
                            # flagWhile=1，本次循环产生完整的模式出现位置，将其记录在occurrencePosition中
                            occurrencePosition.append([newpatternAllPosition[i][0]])
                            newpatternAllPosition[i].pop(0)
                            i += 1
                    if flagWhile:
                        # flagWhile = 1，走到这一步说明新模式在序列patternIndex中有一个完整的出现生成，并将其存入newPatternPosition[patternIndex]中
                        if not newPatternPosition[patternIndex]:
                            newPatternPosition[patternIndex] = occurrencePosition
                        else:
                            for j in range(0, sizeOfPattern):
                                newPatternPosition[patternIndex][j] = newPatternPosition[patternIndex][j] + \
                                                                      occurrencePosition[j]
                    else:
                        # flagWhile = 0 表示生成完成一次性出现挖掘的过程未挖掘出完整的出现，此时需要将occurrencePosition和newpatternAllPosition
                        # 中的位置存入newPatternDeletePosition[patternIndex]中
                        for itemSetNum in range(0, sizeOfPattern):
                            if itemSetNum < len(occurrencePosition):
                                newPatternDeletePosition[patternIndex][itemSetNum] += newpatternAllPosition[
                                                                                          itemSetNum] + \
                                                                                      occurrencePosition[itemSetNum]
                            else:
                                newPatternDeletePosition[patternIndex][itemSetNum] += newpatternAllPosition[
                                    itemSetNum]
                for itemsIndex in range(0, sizePattern(newPattern)):
                    if newpatternAllPosition[itemsIndex]:
                        newPatternDeletePosition[patternIndex][itemsIndex] = sorted(
                            list(set(newpatternAllPosition[itemsIndex])
                                 .union(set(newPatternDeletePosition[patternIndex][itemsIndex]))))
                if not newPatternPosition[patternIndex]:
                    newPatternPosition.pop(patternIndex)
                elif not newPatternPosition[patternIndex][0]:
                    newPatternPosition.pop(patternIndex)
        au = auCalculate(newPattern, newPatternPosition)
        msub = mtb(newPattern, newPatternPosition)
        if msub > minau:
            if au > minau:
                minau = saveTopkPattern(newPattern, ListsTemp, au, minau)
            cPIL.append([newPattern, index + 1, newPatternPosition, msub, newPatternDeletePosition])
    return minau


def HATKMAIN():
    # 保存高平均效用模式
    # 初始化变量
    global cPIL, allItemList, candidatePatternNum, ListsTemp

    minau = 0
    # 生成1-长度的序列
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
                minau = saveTopkPattern([[item]], ListsTemp, au, minau)
            cPIL.append([[[item]], list(utilityTable.keys()).index(item) + 1, position, msub, deletePosition])
    while cPIL:
        msub = cPIL[0][3]
        if msub > minau:
            minau = EP(ListsTemp, minau)
        cPIL.pop(0)
    return ListsTemp

    # fn = [['../Data/OnlineRetail2DatasetUtility.txt', '../Data/OnlineRetail2Dataset.txt'],
    #       ['../Data/OnlineRetail1Dataset.txt', '../Data/OnlineRetail1DatasetUtility.txt'],
    #       ['../Data/DS10L1S6L8I5000F-utility.txt', '../Data/DS10L1S6L8I5000F.txt'],
    #       ['../Data/creatData2Utility.txt', '../Data/creatData2.txt'],
    #       ['../Data/creatData3Utility.txt', '../Data/creatData3.txt']]
    # kL = [[2, 5, 10, 50, 100, 200, 500],
    #       [2, 4, 8, 16, 32, 64, 128],
    #       [2, 4, 6, 8, 10, 12, 14, 16],
    #       [10, 20, 30, 40, 50, 60, 70],
    #       [5, 10, 20, 40, 80, 160, 320]]


if __name__ == '__main__':
    fn = [['../Data/example/3Utility.txt', '../Data/example/3.txt']]
    kL = [[1]]
    kValue = 0
    for i in range(0, len(fn)):
        for kValue in kL[i]:
            utilityTable = DP.operateUtilityTableFile1(fn[i][0])
            dataTable = DP.operateDataFile1(utilityTable, fn[i][1])
            cPIL = []
            ListsTemp = [[], []]
            allItemList = [[], []]
            candidatePatternNum = 0
            starTime = time.time()
            # maxs = memory_usage(HATKMAIN, max_usage=True)
            HATKMAIN()
            endTime = time.time()
            print("k = " + str(kValue) + ", " + fn[i][1])
            with open("../Result/TOAP-result1.txt", 'a') as f:
                f.write("\n----------------------------------------------------------------------\n")
                f.write("k = " + str(kValue) + ", " + fn[i][1] + "\n")
                # f.write(str(int(maxs)) + "\t" + str((endTime - starTime)) + "\t" + str(candidatePatternNum) + "\n")
                f.write(str(ListsTemp))