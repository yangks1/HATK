import random


def creatUtileeTable():
    utileeTable = {}
    for i in range(0, 20):
        item = random.randint(1000, 2000)
        valeee = random.randint(10, 10000)/10
        utileeTable[str(item)] = float(valeee)
    with open("../Data/creatData2Utility.txt", "w") as l:
        j = 0
        for i in utileeTable.keys():
            if j == len(utileeTable)-1:
                l.write(i + "\t" + str(utileeTable[i]))
            else:
                l.write(i + "\t" + str(utileeTable[i]) + "\n")
                j += 1
    return utileeTable


def creatSequence(utileeTable):
    sequenceNum = random.randint(10000, 12000)
    dataTable = []
    L = list(utileeTable.keys())
    for i in range(0, sequenceNum):
        sequence = ""
        itemSetNum = random.randint(2, 50)
        for j in range(0, itemSetNum):
            itemNum = random.randint(1, 7)
            L1 = L[:]
            for k in range(0, itemNum):
                item = random.choice(L1)
                L1.remove(item)
                sequence += item + " "
            sequence += "-1 "
        dataTable.append(sequence)
    with open("../Data/creatData2.txt", "w") as l:
        for i in dataTable:
            l.write(i + "\n")
    return dataTable


utileeTable = creatUtileeTable()
dataT = creatSequence(utileeTable)

