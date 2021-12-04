import time
import DataProcessing as DP
'''
最初版本
'''
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


def supportCalculate(patternPosition):
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
    supportValue = supportCalculate(patternPosition)
    utilityValue = utility(pattern)
    length = lenPattern(pattern)
    averageUtility = (supportValue * utilityValue) / length
    return averageUtility


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
    supportValue = supportCalculate(patternPositionTemp)
    maxUtilityOfOne = maxCode
    maub = maxUtilityOfOne * supportValue
    return maub


def saveTopkPattern(pattern, ListsTemp, au, minau):
    lengthOfList = len(ListsTemp[0])
    global flag
    if lengthOfList < kValue:
        indexTemp = 0
        while indexTemp < lengthOfList and ListsTemp[1][indexTemp] > au:
            indexTemp += 1
        ListsTemp[0].insert(indexTemp, pattern)
        ListsTemp[1].insert(indexTemp, au)
        if lengthOfList + 1 == kValue:
            minau = ListsTemp[1][kValue - 1]
            flag = 1
    else:
        indexTemp = 0
        while indexTemp < lengthOfList and ListsTemp[1][indexTemp] > au:
            indexTemp += 1
        if indexTemp <= lengthOfList:
            ListsTemp[0].insert(indexTemp, pattern)
            ListsTemp[1].insert(indexTemp, au)
            ListsTemp[0].pop()
            ListsTemp[1].pop()
        minau = ListsTemp[1][kValue-1]
        flag = 1
    return minau


def oneOff(itemSetExitInter, newPatternPosition, newpatternAllPosition):
    """
    一次性判断
    满足一次性返回True，否则返回False

    :param itemSetExitInter:
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


def extendPattern(ListsTemp, minau):
    """
    模式增长

    :param ListsTemp: top-k个模式及其平均效用值
    :param minau: 最小支持度阈值
    :return:
    """
    global candidatePatternNum
    patternInfor = candidatePatternInforList[0]
    sizeOfPattern = len(patternInfor[0])
    oldPatternPosition = patternInfor[2]
    oldPatternDeletePosition = patternInfor[4]

    # 序列扩展
    for item in allItemName.keys():
        if item not in deletedItemSet:
            # 得到newPattern
            newPattern = patternInfor[0][:]
            newPattern.append([item])
            # 初始化
            newPatternPosition = {}
            newPatternDeletePosition = {}
            itemPosition = dataTable[item]
            indexOfItem = list(allItemName.keys()).index(item)
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
                if patternIndex in itemPosition.keys():   # 确保pattern和新增加的元素在同一个序列中出现
                    newPatternPosition[patternIndex] = []
                    newPatternDeletePosition[patternIndex] = []
                    for i in range(0, sizeOfPattern + 1):
                        newPatternDeletePosition[patternIndex].append([])
                    # 生成新模式中各项集出现的所有位置集合
                    newpatternAllPosition = []
                    for itemSetNum in range(0, sizeOfPattern):
                        newpatternAllPosition.append(oldPatternPosition[patternIndex][:][itemSetNum][:] + oldPatternDeletePosition[patternIndex][:][itemSetNum][:])
                    newpatternAllPosition.append(itemPosition[patternIndex][0][:])

                    flagWhile = 1
                    while flagWhile and newpatternAllPosition[0]:
                        occurrencePosition = []

                        # 对每个序列的第一个项集进行查找可以使用的位置
                        i = 0
                        while flagWhile and newPatternPosition[patternIndex] and not oneOff(itemSetExitInter[i], newPatternPosition[patternIndex], newpatternAllPosition[i]):
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
                                    while flagWhile and (newpatternAllPosition[i][0] <= occurrencePosition[i-1][0] or not oneOff(itemSetExitInter[i], newPatternPosition[patternIndex], newpatternAllPosition[i])):
                                        newPatternDeletePosition[patternIndex][i].append(newpatternAllPosition[i][0])
                                        newpatternAllPosition[i].pop(0)
                                        if not newpatternAllPosition[i]:
                                            # 若第i+1个项集没有可扩展的位置时，flagWhile = 0
                                            flagWhile = 0
                                else:
                                    while flagWhile and newpatternAllPosition[i][0] <= occurrencePosition[i-1][0]:
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
                                    newPatternPosition[patternIndex][j] = newPatternPosition[patternIndex][j] + occurrencePosition[j]
                        else:
                            # flagWhile = 0 表示生成完成一次性出现挖掘的过程未挖掘出完整的出现，此时需要将occurrencePosition和newpatternAllPosition中的位置存入newPatternDeletePosition[patternIndex]中
                            for itemSetNum in range(0, sizeOfPattern+1):
                                if itemSetNum < len(occurrencePosition):
                                    newPatternDeletePosition[patternIndex][itemSetNum] += newpatternAllPosition[itemSetNum] + \
                                                                                          occurrencePosition[itemSetNum]
                                else:
                                    newPatternDeletePosition[patternIndex][itemSetNum] += newpatternAllPosition[
                                        itemSetNum]

                    if not newPatternPosition[patternIndex]:
                        newPatternPosition.pop(patternIndex)
                        newPatternDeletePosition.pop(patternIndex)
                    elif not newPatternPosition[patternIndex][0]:
                        newPatternPosition.pop(patternIndex)
                        newPatternDeletePosition.pop(patternIndex)
            au = auCalculate(newPattern, newPatternPosition)
            maub = maubCalculate(newPatternPosition)
            if maub > minau:
                if au > minau:
                    minau = saveTopkPattern(newPattern, ListsTemp, au, minau)
                candidatePatternInforList.append([newPattern, indexOfItem + 1, newPatternPosition, maub, newPatternDeletePosition])
                candidatePatternNum += 1
    # 项集扩展
    for item in list(allItemName.keys())[patternInfor[1]:]:
        if item not in deletedItemSet:
            # 得到newPattern
            newPattern = patternInfor[0][:sizeOfPattern-1]
            newPattern.append(patternInfor[0][sizeOfPattern-1][:])
            newPattern[sizeOfPattern-1].append(item)

            newPatternPosition = {}
            newPatternDeletePosition = {}
            itemPosition = dataTable[item]
            indexOfItem = list(allItemName.keys()).index(item)

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
                                                                                            newPatternPosition[patternIndex],
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
                            # flagWhile = 0 表示生成完成一次性出现挖掘的过程未挖掘出完整的出现，此时需要将occurrencePosition和newpatternAllPosition中的位置存入newPatternDeletePosition[patternIndex]中
                            for itemSetNum in range(0, sizeOfPattern):
                                if itemSetNum < len(occurrencePosition):
                                    newPatternDeletePosition[patternIndex][itemSetNum] += newpatternAllPosition[
                                                                                              itemSetNum] + \
                                                                                          occurrencePosition[itemSetNum]
                                else:
                                    newPatternDeletePosition[patternIndex][itemSetNum] += newpatternAllPosition[
                                        itemSetNum]

                    if not newPatternPosition[patternIndex]:
                        newPatternPosition.pop(patternIndex)
                    elif not newPatternPosition[patternIndex][0]:
                        newPatternPosition.pop(patternIndex)
            au = auCalculate(newPattern, newPatternPosition)
            maub = maubCalculate(newPatternPosition)
            if maub > minau:
                if au > minau:
                    minau = saveTopkPattern(newPattern, ListsTemp, au, minau)
                candidatePatternInforList.append([newPattern, indexOfItem + 1, newPatternPosition, maub, newPatternDeletePosition])
                candidatePatternNum += 1
    return minau


# 主算法
def HATKMAIN():
    # 保存高平均效用模式
    # 初始化变量
    global candidatePatternInforList, flag, minutal, candidatePatternNum
    ListsTemp = [[], []]
    minau = 0
    # 生成1-长度的序列
    for item in allItemName.keys():
        deletePosition = {}
        position = {}
        for dt in dataTable[item]:
            position[dt] = dataTable[item][dt]
            deletePosition[dt] = [[]]
        maub = maubCalculate(position)
        allItemName[item] = maub
        au = auCalculate([[item]], position)
        if maub > minau:
            if au > minau:
                minau = saveTopkPattern([[item]], ListsTemp, au, minau)
            candidatePatternInforList.append([[[item]], list(allItemName.keys()).index(item) + 1, position, maub, deletePosition])
            candidatePatternNum += 1
    # 模式增长，
    while candidatePatternInforList:
        if flag and minutal < minau:
            minutal = maxCode
            for name in allItemName.keys():
                if name not in deletedItemSet:
                    if allItemName[name] < minau:
                        deletedItemSet.append(name)
                    elif allItemName[name] < minutal:
                            minutal = allItemName[name]
            flag = 0
        maub = candidatePatternInforList[0][3]
        if maub >= minau:
            minau = extendPattern(ListsTemp, minau)
        candidatePatternInforList.pop(0)
    return ListsTemp


if __name__ == '__main__':

    # 小型例子
    # utilityTable = {"a": 6, "b": 1, "c": 5, "d": 2, "e": 4, "f": 3}
    # dataTable = {"a": {"1": [[1, 2, 3]], "2": [[1, 2]], "3": [[2, 3]], "4": [[1, 4]], "5": [[2]]}, "b": {"1": [[2, 3]], "2": [[2, 3]], "3": [[2, 3]], "4": [[2]], "5": [[1, 3]]}, "c": {"1": [[1, 2, 5]], "2": [[3]], "4": [[3, 4]], "5": [[3, 5]]}, "d": {"1": [[3]], "2": [[2, 3]], "3": [[3]], "4": [[3]], "5": [[2, 5]]}, "e": {"1": [[4]], "2": [[1, 3]], "4": [[2]], "5": [[1, 2, 3]]}, "f": {"1": [[5]], "3": [[1]], "5": [[4]]}}
    # utilityTable = {"a": 2.1, "b": 1.2}
    # dataTable = {"a": {"1": [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]]}, "b": {"1": [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]]}}

    # 数据库预处理
    utilityTable = DP.operateUtilityTableFile1()
    dataTable = DP.operateDataFile1(utilityTable)
    # utilityTable = DP.operateUtilityTableFile2()
    # dataTable = DP.operateDataFile2(utilityTable)
    # utilityTable = DP.operateUtilityTableFile3()
    # dataTable = DP.operateDataFile3(utilityTable)

    # k值
    kValue = 2
    # kValue = len(utilityTable)

    # candidatePatternInforList存储候选模式，及其信息：
    # [模式pattern, 可进行I-扩展的元素, 模式pattern的出现位置信息, 模式pattern的平均效用, 最大平均效用上界maub, 模式pattern各项集未在一次性中使用的位置集合]
    candidatePatternInforList = []
    # allItemName 中存放字符集以及每个字符的maub值
    # 可优化 deletedItemSet可以存入allItemName，用0,1表示是否可扩展
    allItemName = utilityTable.copy()
    # 存放字符集中不考虑扩展的字符集合
    deletedItemSet = []

    maxCode = maxuCalculate()
    flag = 0    # 纪录minau值是否改变
    # 可优化：minutal可以不使用
    minutal = 0     # 纪录字符集中可扩展的字符中maub的最小值
    candidatePatternNum = 0     # 记录生成候选模式数量

    starTime = time.time()
    Lists = HATKMAIN()
    endTime = time.time()

    print("生成的候选模式个数：" + str(candidatePatternNum))
    print("运行时间：" + str(endTime * 1000-starTime * 1000) + "ms")
    print(Lists)
