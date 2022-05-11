if __name__ == '__main__':

    utilityTable1 = {}
    utilityTable2 = {}
    with open("../Data/Sds1-utility.txt", "r") as f1:
        for i in f1.readlines():
            name = i.split('\t', 1)[0]
            utilityTable1[name] = 0.0
    with open("../Data/onlineUtilityTable1.txt", "r") as f2:
        for i in f2.readlines():
            name = i.split('\t', 1)[0]
            utilityTable2[name] = float(i.split('\t', 1)[1])
    with open("../Data/Sds1-utility.txt", "w") as f3:
        j = 0
        for i in utilityTable1.keys():
            # print(str(list(utilityTable2.keys())[j]))
            # print(utilityTable2[list(utilityTable2.keys())[j]])
            f3.write(i + "\t" + str(utilityTable2[list(utilityTable2.keys())[j]]) + "\n")
            j += 1
            if j == len(list(utilityTable2.keys())):
                j = 0
    max1 = 0
    min1 = 10000000
    for i in utilityTable1.keys():
        if utilityTable1[i] > max1:
            # if utilityTable[i] == 1000000000.0:
            #     print(1000000000000.0)
            max1 = utilityTable1[i]
            # if max1 == 1000000000.0:
            #     print(1000000000000.0)
        if utilityTable1[i] < min1:
            min1 = utilityTable1[i]
    print("max:" + str(max1) + "   min:" + str(min1))