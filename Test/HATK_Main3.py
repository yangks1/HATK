# 读取效用表
import time


def operateUtilityTableFile():
    with open("../Data/onlineUtilityTable.txt", 'r') as f1:
        global utilityTable
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
def operateDataFile():  # 处理序列数据库
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
    计算模式pattern长度

    :param pattern: 模式pattern
    :return: 模式pattern的长度
    """
    lengthOfPattern = 0
    for itemSets in pattern:
        lengthOfPattern += len(itemSets)
    return lengthOfPattern


def auCalculate(pattern, patternPositionTemp):
    """
    计算模式pattern的平均效用

    :param patternPositionTemp: 模式pattern的出现位置纪录
    :param pattern: 模式pattern
    :return: 模式pattern的平均效用
    """
    supportValue = supportCalculate(patternPositionTemp)
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


def maubCalculate(pattern, patternPositionTemp):
    """
    计算最大平均效用上界maub

    :param patternPositionTemp: 模式pattern的出现位置纪录
    :param pattern: 模式pattern
    :return: maub（pattern）
    """
    supportValue = supportCalculate(patternPositionTemp)
    maxUtilityOfOne = maxuCalculate()
    length = lenPattern(pattern)
    maub = (maxUtilityOfOne * supportValue) / length
    return maub


def saveTopkPattern(pattern, ListsTemp, au, minau):
    lengthOfList = len(ListsTemp[0])
    if lengthOfList < kValue:
        indexTemp = 0
        while indexTemp < lengthOfList and ListsTemp[1][indexTemp] > au:
            indexTemp += 1
        ListsTemp[0].insert(indexTemp, pattern)
        ListsTemp[1].insert(indexTemp, au)
        if lengthOfList == kValue:
            minau = ListsTemp[1][kValue - 1]
    else:
        indexTemp = 0
        while indexTemp < lengthOfList and ListsTemp[1][indexTemp] > au:
            indexTemp += 1
        if indexTemp < lengthOfList:
            ListsTemp[0].insert(indexTemp, pattern)
            ListsTemp[1].insert(indexTemp, au)
            ListsTemp[0].pop()
            ListsTemp[1].pop()
            minau = ListsTemp[1][kValue-1]
    return ListsTemp, minau


def extendPattern(ListsTemp, minau):
    """
    模式增长函数

    :param ListsTemp: top-k个模式及其平均效用值
    :param minau: 最小支持度阈值
    :return:
    """
    patternInfor = candidatePatternInforList[0]
    length = lenPattern(patternInfor[0])
    oldPatternPosition = patternInfor[2]
    # 序列扩展
    for item in allItemName:
        # 得到newPattern
        newPattern = patternInfor[0]
        newPattern.append([item])
        newPatternPosition = {}
        itemPosition = dataTable[item]
        indexOfItem = allItemName.index(item)
        """
        oldPatternPosition[patternIndex]表示pattern在序列号为patternIndex的出现位置信息[[1, 5], [2, 6], [3, 7]]
        itemPosition[patternIndex]表示pattern新增元素s在序列号为patternIndex的出现位置信息如a：[1, 5, 7]
        newPatternPosition[patternIndex]表示增长后的新序列newPattern在序列号为patternIndex的出现位置信息如[[1], [2], [3], [5]]
        """
        # 算出patternPosition
        for patternIndex in oldPatternPosition.keys():
            '''此循环使得patternIndex遍历包含oldPattern的序列号'''
            if patternIndex in itemPosition.keys():   # 确保pattern和新增加的元素在同一个序列中出现
                '''if语句确保oldPattern和itme出现在同一个序列中'''
                newPatternPosition[patternIndex] = []
                occurrenceId = 0
                if length != len(oldPatternPosition[patternIndex]):
                    print("这里不等 2")
                for i in oldPatternPosition[patternIndex][length - 1]:   # 对pattern的每一个出现进行依次增加元素，i为这次出现最后一项元素的位置
                    '''此循环i遍历oldPattern的最后一个项集在序列号为patternIndex出现的位置集合'''
                    for j in itemPosition[patternIndex][0]:
                        '''此循环j遍历新增加项itme在序列号为patternIndex出现的位置集合'''
                        if j > i:                          # 寻找新增加的元素出现位置在i之后的位置j
                            if occurrenceId == 0:              # 若为新增的第一列，需要增加列表存储
                                for t in range(0, length-1):
                                    newPatternPosition[patternIndex].append([oldPatternPosition[patternIndex][t][occurrenceId]])
                                newPatternPosition[patternIndex].append([j])
                            else:
                                for t in range(0, length):
                                    newPatternPosition[patternIndex][t].append(oldPatternPosition[patternIndex][t][occurrenceId])
                                newPatternPosition[patternIndex].append([j])
                            break
                    occurrenceId += 1
                    if length != len(oldPatternPosition[patternIndex]):
                        print("这里不等 1")
                if not newPatternPosition[patternIndex]:
                    newPatternPosition.pop(patternIndex)
                if length != len(oldPatternPosition[patternIndex]):
                    print("这里不等 1")
        au = auCalculate(newPattern, newPatternPosition)
        maub = maubCalculate(newPattern, newPatternPosition)
        if au > maub:
            if au > minau:
                ListsTemp, minau = saveTopkPattern(newPattern, ListsTemp, au, minau)
            if indexOfItem == len(allItemName) - 1:
                candidatePatternInforList.append([newPattern, indexOfItem + 1, newPatternPosition])
            else:
                candidatePatternInforList.append([newPattern, indexOfItem + 1, newPatternPosition])
    for item in allItemName[patternInfor[1]:]:
        # 得到newPattern
        newPattern = patternInfor[0]
        newPattern[length-1].append(item)
        newPatternPosition = {}
        itemPosition = dataTable[item]
        indexOfItem = allItemName.index(item)
        for patternIndex in oldPatternPosition.keys():
            if patternIndex in itemPosition.keys():   # 确保pattern和新增加的元素在同一个序列中出现
                newPatternPosition[patternIndex] = []
                # 取交集
                intersectionOfposition = list(set(oldPatternPosition[patternIndex][length - 1]).intersection(itemPosition[patternIndex][0]))
                for endposition in intersectionOfposition:
                    endIndex = oldPatternPosition[patternIndex][length - 1].index(endposition)
                    if newPatternPosition[patternIndex]:                         # 若为新增的第一列，需要增加列表存储
                        for t in range(0, length-1):
                            newPatternPosition[patternIndex].append([oldPatternPosition[patternIndex][t][endIndex]])
                    else:
                        for t in range(0, length-1):
                            newPatternPosition[patternIndex][t].append(oldPatternPosition[patternIndex][t][endIndex])

                if not newPatternPosition[patternIndex]:
                    newPatternPosition.pop(patternIndex)
        au = auCalculate(newPattern, newPatternPosition)
        maub = maubCalculate(newPattern, newPatternPosition)
        if au > maub:
            if au > minau:
                ListsTemp, minau = saveTopkPattern(newPattern, ListsTemp, au, minau)
            if indexOfItem == len(allItemName) - 1:
                candidatePatternInforList.append([newPattern, indexOfItem + 1, newPatternPosition])
            else:
                candidatePatternInforList.append([newPattern, indexOfItem + 1, newPatternPosition])
    return ListsTemp, candidatePatternInforList, minau


# 主算法
def HATKMAIN():
    # 保存高平均效用模式
    # 初始化变量
    ListsTemp = [[], []]
    global candidatePatternInforList
    minau = 0
    # 生成1-长度的序列
    for item in allItemName:
        position = {}
        for dt in dataTable[item]:
            position[dt] = dataTable[item][dt]
        maub = maubCalculate([[item]], position)
        au = auCalculate([[item]], position)
        if maub > minau:
            if au > minau:
                ListsTemp, minau = saveTopkPattern([[item]], ListsTemp, au, minau)
            candidatePatternInforList.append([[[item]], allItemName.index(item) + 1, position])
    # 模式增长，
    # inttt = 0
    while candidatePatternInforList:
        # if inttt == 10:
        #     break
        # inttt += 1
        nowPattern = candidatePatternInforList[0][0]
        maub = maubCalculate(nowPattern, candidatePatternInforList[0][2])
        if maub >= minau:
            ListsTemp, candidatePatternInforList, minau = extendPattern(ListsTemp, minau)
        candidatePatternInforList.pop(0)
    return ListsTemp


if __name__ == '__main__':

    # utilityTable = {"a": 6, "b": 1, "c": 5, "d": 2, "e": 4, "f": 3}
    # dataTable = {"a": {"1": [[1,2,3]], "2": [[1,2]], "3":[[2,3]], "4":[[1,4]],"5":[[2]]}, "b": {"1":[[2,3]],"2":[[2,3]],"3":[[2,3]],"4":[[2]],"5":[[1,3]]}, "c": {"1":[[1,2,5]],"2":[[3]],"4":[[3,4]],"5":[[3,5]]}, "d": {"1":[[3]],"2":[[2,3]],"3":[[3]],"4":[[3]],"5":[[2,5]]}, "e": {"1":[[4]],"2":[[1,3]],"4":[[2]],"5":[[1,2,3]]}, "f": {"1":[[5]],"3":[[1]],"5":[[4]]}}

    # 数据库预处理
    # 存储所有出现位置
    utilityTable = operateUtilityTableFile()
    dataTable = operateDataFile()

    kValue = 1
    # kValue = len(utilityTable)

    candidatePatternInforList = []
    '''candidatePatternInforList存储候选模式，及其信息：[模式pattern, 可进行I-扩展的元素, 模式pattern的出现位置信息, 模式pattern的平均效用, 最大平均效用上界maub]'''
    allItemName = list(utilityTable.keys())
    allItemName.sort()

    starTime = time.time()
    Lists = HATKMAIN()
    endTime = time.time()

    print(Lists)
    print("运行时间：" + str(int(endTime) * 1000-int(starTime) * 1000) + "ms")
