import random


def creatUtileeTable():
    utileeTable = {}
    for i in range(0, 10):
        item = random.randint(1000, 2000)
        valeee = random.randint(10, 1000)/10
        utileeTable[str(item)] = float(valeee)
    with open("../Data/creatDataUtility.txt", "w") as l:
        j = 0
        for i in utileeTable.keys():
            if j == len(utileeTable)-1:
                l.write(i + "\t" + str(utileeTable[i]))
            else:
                l.write(i + "\t" + str(utileeTable[i]) + "\n")
                j += 1
    return utileeTable


def creatSequence(utileeTable):
    sequenceNum = 100
    dataTable = []
    for i in range(0, sequenceNum):
        sequence = ""
        itemSetNum = random.randint(10, 20)
        for j in range(0, itemSetNum):
            itemNum = random.randint(5, 8)
            for k in range(0, itemNum):
                item = random.choice(list(utileeTable))
                sequence += item + " "
            sequence += "-1 "
        dataTable.append(sequence)
    with open("../Data/creatData.txt", "w") as l:
        j = 0
        for i in dataTable:
            l.write(i + "\n")
    return dataTable


utileeTable = creatUtileeTable()
print(utileeTable)
dataT = creatSequence(utileeTable)
print(dataT)
