import random


def op():

    with open("SDB2.txt", 'r') as f:


        data = []
        listData = []
        utility = {}
        for line in f.readlines():
            line = line.strip('\n')
            data.append(line)
        for sequence in data:

            newSequence = ""
            for s in sequence:
                if s != ' ':
                    if s not in utility.keys():
                        utility[s] = float(random.randint(100, 2000))/100
                    if s == sequence[-1]:
                        newSequence += s
                    else:
                        newSequence += s + ' -1 '
            listData.append(newSequence)

        with open('sd.txt', 'w') as l:
            for new in listData:
                l.write(new + "\n")
        with open("../Data/proteinUtility.txt", "w") as l:
            for k in utility.keys():
                l.write(k + "\t" + str(utility[k]) + "\n")





op()