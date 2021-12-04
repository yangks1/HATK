def operateUtilityTableFile():
    with open("utilityTable100.txt", 'r') as f1:
        utilityTable = {}
        for i in f1.readlines():
            name = i.split('\t', 1)[0]
            price = float(i.split('\t', 1)[1])
            utilityTable[name] = price
    return utilityTable


def operateDataFile():
    dataTableTemp = []
    uTT = utilityTable.keys()
    with open("../Data/online-utility.txt", 'r') as f2:
        for sequence in f2.readlines():
            string = ""  # 用于记录读取出的字符串
            sequenceString = ""
            for letter in sequence:
                if letter != " ":
                    string += letter
                elif string == "-1" or string in uTT:
                    sequenceString += string + " "
                    string = ""
            if sequenceString:
                dataTableTemp.append(sequenceString)
    with open("online-utility100.txt", 'w') as l:
        j = 0
        for i in dataTableTemp:
            if j == 99:
                l.write(i)
            else:
                l.write(i + "\n")
            j += 1

utilityTable = operateUtilityTableFile()
operateDataFile()

