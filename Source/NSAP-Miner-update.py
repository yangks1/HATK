import time
import sys
from Tool import Pdata

pdata = Pdata.processingData()

# 挖掘（长度为1的频繁-》S-连接-》I-连接）
def Min_FP(SeqNum, S, sort_item, minau, U):
    P = {}    #存储模式的出现位置
    LP = {}   #存储模式的项集子模式的出现位置
    FP = []   #存储频繁模式 可扩展的模式
    FP1 = []  #存储长度为1的频繁模式 用于模式增长
    NSAP = [] #存储高平均效用模式
    max = 0.0   #最大效用
    keys = U.keys()
    for i in keys:
        if max < float(U[i]):
            max = float(U[i])
    minsup = minau / max
    CanNum = 0
    # SeqNum = len(lines_s)
    count = 0
    for i in sort_item:
        CanNum += 1
        for j in range(SeqNum):
            count += len(S[i][j])
        if count >= minsup:
            FP1.append(i)
            FP.append(i)
            P[i] = [[] for k in range(SeqNum)]
            P[i] = S[i]
            LP[i] = [[] for k in range(SeqNum)]
            for k in range(SeqNum):
                for t in range(len(P[i][k])):
                    LP[i][k].append(P[i][k][t] -1)
            # print(i + ':' + str(utility[i]))
            au = float(U[i]) * count
            if au >= minau:
                NSAP.append(i)
        count = 0
    # for i in range(1162, len(utility)):
    #     print(utility[i])
    flag = 0
    print(FP1)
    for fp in FP: # fp: str
        for item in FP1: # item: str
            pattern = fp + " -1 " + item # S连接**************************************
            CanNum += 1
            LP[pattern] = [[] for k in range(SeqNum)]
            LP[pattern] = P[fp]
            P[pattern] = [[] for i in range(SeqNum)]
            for i in range(SeqNum):
                for j in range(len(P[fp][i])):
                    if flag == len(S[item][i]):
                        # flag = 0
                        break
                    for k in range(flag, len(S[item][i])):
                        if S[item][i][k] > P[fp][i][j]:
                            P[pattern][i].append(S[item][i][k])
                            count += 1
                            flag = k+1
                            break
                        if k == len(S[item][i]) - 1:
                            flag = len(S[item][i])
                flag = 0
            if count >= minsup:
                # if pattern == '10 -1 28':
                # print(pattern, ': count=', count)
                # print(P[pattern])
                # print('count=' + str(count))
                # print("**********")
                FP.append(pattern)
                au = 0
                pnum = 0
                pat = pattern.strip().split(' ')
                for m in pat:
                    if m != '-1':
                        pnum += 1
                        au += float(U[m])
                au = au * count / pnum
                if au >= minau:
                    NSAP.append(pattern)
                    # if pattern == '10 -1 28':
                    #     print (pattern + ': ', end = "")
                    #     print (P[pattern])
                    #     print ('count=' + str(count) + '  ' + 'au=' + str(au))
                    #     print ("**********")
                    # 输出模式，出现位置，支持度，和平均效用值
                    # print (pattern + ': ', end = "")
                    # # print (P[pattern])
                    # print ('count=' + str(count) + '  ' + 'au=' + str(au))
                    # print ("**********")
            else:
                del P[pattern]
                del LP[pattern]
            count = 0
            if fp.split()[len(fp.split())-1] < item: # I连接************************************
                CanNum += 1
                pattern = fp + ' ' + item
                LP[pattern] = [[] for i in range(SeqNum)]
                LP[pattern] = LP[fp]
                P[pattern] = [[] for i in range(SeqNum)]
                unit = S[item][:]    # [:]:复制字典中的内容
                pattern_array = fp.strip().split(' ')
                f = -1
                for i in range(len(pattern_array)):
                    if pattern_array[i] == '-1':
                        f = i
                for i in range(f+1, len(pattern_array)):
                    for j in range(len(unit)):
                        unit[j] = sorted(list(set(unit[j]) & set(S[pattern_array[i]][j])))
                for i in range(SeqNum):
                    for j in range(len(LP[fp][i])):
                        if flag == len(unit[i]):
                            break
                        for k in range(flag, len(unit[i])):
                            if unit[i][k] > LP[fp][i][j]:
                                P[pattern][i].append(unit[i][k])
                                count += 1
                                flag = k + 1
                                break
                            if k == len(unit[i]) - 1:
                                flag = len(unit[i])
                    flag = 0
                if count >= minsup:
                    # print(pattern, ': count=', count)
                    FP.append(pattern)
                    au = 0
                    pnum = 0
                    pat = pattern.strip().split(' ')
                    for m in pat:
                        if m != '-1':
                            pnum += 1
                            au += float(U[m])
                    au = au * count / pnum
                    if au >= minau:
                        NSAP.append(pattern)
                        # 输出模式，出现位置，支持度，和平均效用值
                        # if pattern == '10 -1 28':
                        # print (pattern + ': ', end = "")
                        # # print (P[pattern])
                        # print ('count=' + str(count) + '  ' + 'au=' + str(au))
                        # print ("**********")
                else:
                    del P[pattern]
                    del LP[pattern]
            count = 0
        del P[fp]
        del LP[fp]
    print("High average utility patterns:", end = " ")
    print(NSAP)
    print("Frequent patterns:", end=" ")
    print(FP)
    print("Number of high average utility patterns: " + str(len(NSAP)))
    print("Number of frequent patterns: " + str(len(FP)))
    print("Number of candidate patterns: " + str(CanNum))


if __name__ == '__main__':
    fn = [['../Data/u.txt', '../Data/test.txt'],
          ['../Data/chainstoreUtility.txt', '../Data/chainstore.txt'],
          ['../Data/MicroblogPCUUtility.txt', '../Data/MicroblogPCU.txt'],
          ['../Data/Online2Utility.txt', '../Data/Online-2.txt'],
          ['../Data/onlineUtilityTable.txt', '../Data/online-utility.txt'],
          ['../Data/Sds1-utility.txt', '../Data/Sds1.txt'],
          ['../Data/Sds2-utility.txt', '../Data/Sds2.txt'],
          ['../Data/Sds3-utility.txt', '../Data/Sds3.txt'],
          ['../Data/Sds4-utility.txt', '../Data/Sds4.txt'],
          ['../Data/creatDataUtility1.txt', '../Data/creatData1.txt'],
          ['../Data/creatDataUtility2.txt', '../Data/creatData2.txt'],
          ['../Data/creatDataUtility3.txt', '../Data/creatData3.txt'],
          ['../Data/creatDataUtility4.txt', '../Data/creatData4.txt']]
    kL = [10, 50, 100, 200, 500, 1000, 1500, 2000, 25000, 3000]
    kValue = 0
    for i in range(0, len(fn)):
        for kValue in kL:
            minau = 0
            readFileName0 = fn[i][0]
            readFileName1 = fn[i][1]
            S = {}
            U = {}
            SeqNum, S, sort_item = pdata.datap(readFileName1, S)
            pdata.utilityp(readFileName0, U)
            starttime = time.time()
            Min_FP(SeqNum, S, sort_item, int(minau), U)  # SeqNum:序列数 S:数据集位置字典 sort_item:排序后的字符集 minau:最小平均效用阈值 U:效用字典
            endtime = time.time()
            print("Running time: " + str(int(round(endtime * 1000)) - int(round(starttime * 1000))) + "ms")
