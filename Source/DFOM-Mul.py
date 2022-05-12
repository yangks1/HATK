import re
import time
import sys
import json
from collections import defaultdict, OrderedDict
import json
import Pdata
pdata = Pdata.processingData()
def pares(a,s,k,q):
    for j in range(k,len(s)):
        if a < s[j]:
            q.append(s[j])
            flag = j + 1
            return flag, 1
    return 0, 0

# 挖掘（长度为1的频繁-》S-连接-》I-连接）
def Min_FP(SeqNum,S,sort_item,minau,U):
    P = {}    #存储模式的出现位置
    LP = {}   #存储模式的项集子模式的出现位置
    FP = []   #存储频繁模式 可扩展的模式
    FP1 = []  #存储长度为1的频繁模式 用于模式增长
    NSAP = [] #存储高平均效用模式
    max = 0   #最大效用
    keys = U.keys()
    for i in keys:
        if max < int(U[i]):
            max = int(U[i])
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
            au = int(U[i]) * count
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
            # pattern = 'a -1 a c -1 c'
            pattern_array = pattern.strip().split(' -1 ') # ['a c', 'a b d', 'c', 'b']
            # print(pattern_array)
            Nettree = [[[] for i in range(SeqNum)] for k in range(len(pattern_array))]
            unit = [[] for k in range(len(pattern_array))]
            for i in range(len(pattern_array)):
                pat_array = pattern_array[i].strip().split(' ')
                # print(pat_array)
                unit[i] = S[pat_array[0]][:]
                for j in pat_array:
                    for m in range(SeqNum):
                        unit[i][m] = sorted(list(set(unit[i][m]) & set(S[j][m])))
                # print(unit[i])
            flag = -1
            # if pattern == '10 -1 10 -1 44':
            #     print(unit)

            for i in range(SeqNum):
                for m in range(len(unit[0][i])):
                        bbb = 0
                        Nettree[0][i].append(unit[0][i][m])
                        for j in range(1, len(unit)):
                            n = 1
                            if unit[j][i] == []:
                                bbb = 1
                                break
                            else:
                                for k in range(len(unit[j][i])):
                                    if Nettree[j][i] == []:
                                        aaa = -1
                                    else:
                                        aaa = Nettree[j][i][-1]
                                    if unit[j][i][k] > Nettree[j -1][i][-1] and unit[j][i][k] > aaa:
                                        Nettree[j][i].append(unit[j][i][k])
                                        if j == len(unit) - 1:
                                            count += 1
                                        n = 0
                                        break
                                if n:
                                    bbb = 1
                                    break
                        if bbb:
                            break

            if count >= minsup:
                # if pattern == '10 -1 28':
                #     print(pattern + ': ', end="")
                #     print(unit[0][6])
                #     print(unit[1][6])
                #     print('S[28]:', S['28'][6])
                #     print(type(unit[1][6][0]))
                #     print('count=' + str(count))
                #     print("**********")
                FP.append(pattern)
                au = 0
                pnum = 0
                pat = pattern.strip().split(' ')
                for m in pat:
                    if m != '-1':
                        pnum += 1
                        au += int(U[m])
                au = au * count / pnum
                if au >= minau:
                    NSAP.append(pattern)
                    # if pattern == '10 -1 28':
                    # print (pattern + ': ', end = "")
                    # # print (P[pattern])
                    # print ('count=' + str(count) + '  ' + 'au=' + str(au))
                    # print ("**********")
                    # 输出模式，出现位置，支持度，和平均效用值
                    # print (pattern + ': ', end = "")
                    # print (P[pattern])
                    # print ('count=' + str(count) + '  ' + 'au=' + str(au))
                    # print ("**********")
            del Nettree
            del unit
            count = 0
            if fp.split()[len(fp.split())-1] < item: # I连接************************************
                CanNum += 1
                pattern = fp + ' ' + item
                pattern_array = pattern.strip().split(' -1 ')  # ['a c', 'a b d', 'c', 'b']
                # print(pattern_array)
                Nettree = [[[] for i in range(SeqNum)] for k in range(len(pattern_array))]
                unit = [[] for k in range(len(pattern_array))]
                for i in range(len(pattern_array)):
                    pat_array = pattern_array[i].strip().split(' ')
                    # print(pat_array)
                    unit[i] = S[pat_array[0]][:]
                    for j in pat_array:
                        for m in range(SeqNum):
                            unit[i][m] = sorted(list(set(unit[i][m]) & set(S[j][m])))
                    # if pattern_array == ['c', 'a c', 'a c', 'c f']:
                    #     print(unit[i])
                flag = -1
                if len(unit) == 1:
                    for j in range(len(unit[0])):
                        count += len(unit[0][j])
                else:
                    for i in range(SeqNum):
                        flag = -1
                        for m in range(len(unit[0][i])):
                                bbb = 0
                            # if unit[0][i][m] > flag:
                                Nettree[0][i].append(unit[0][i][m])
                                for j in range(1, len(unit)):
                                    n = 1
                                    if unit[j][i] == []:
                                        bbb = 1
                                        break
                                    else:
                                        for k in range(len(unit[j][i])):
                                            # if pattern_array == ['c', 'a c', 'a c', 'c f']:
                                            #     print('Nettree', Nettree[j - 1][i])
                                            #     print('unit', unit[j][i][k])
                                            if Nettree[j][i] == []:
                                                aaa = -1
                                            else:
                                                aaa = Nettree[j][i][-1]
                                            if unit[j][i][k] > Nettree[j - 1][i][-1] and unit[j][i][k] > aaa:
                                                Nettree[j][i].append(unit[j][i][k])
                                                if j == len(unit) - 1:
                                                    count += 1
                                                    flag = unit[j][i][k]
                                                    # print('flag=', flag)
                                                n = 0
                                                break
                                        if n:
                                            bbb = 1
                                            break
                                if bbb:
                                    break
                                # flag = -1
                # print(pattern, ':', Nettree[-1], 'count=', count)
                if count >= minsup:
                    FP.append(pattern)
                    au = 0
                    pnum = 0
                    pat = pattern.strip().split(' ')
                    for m in pat:
                        if m != '-1':
                            pnum += 1
                            au += int(U[m])
                    au = au * count / pnum
                    if au >= minau:
                        NSAP.append(pattern)
                        # 输出模式，出现位置，支持度，和平均效用值
                        # print (pattern + ': ', end = "")
                        # # print (P[pattern])
                        # print ('count=' + str(count) + '  ' + 'au=' + str(au))
                        # print ("**********")
                del Nettree
                del unit
            count = 0
        # del P[fp]
        # del LP[fp]
    print ("High average utility patterns:", end = " ")
    print (NSAP)
    print("Frequent patterns:", end=" ")
    print(FP)
    print ("Number of high average utility patterns: " + str(len(NSAP)))
    print ("Number of frequent patterns: " + str(len(FP)))
    print ("Number of candidate patterns: " + str(CanNum))


if __name__ == '__main__':
    try:
        readFileName1 = sys.argv[1]
        readFileName2 = sys.argv[2]
    except Exception as e:
        print(e)
    S = {}
    U = {}
    SeqNum, S, sort_item = pdata.datap(readFileName1, S)
    pdata.utilityp(readFileName2, U)
    del pdata
    for minau in sys.argv[3:]:
        starttime = time.time()
        Min_FP(SeqNum, S, sort_item, int(minau), U) # SeqNum:序列数 S:数据集位置字典 sort_item:排序后的字符集 minau:最小平均效用阈值 U:效用字典
        endtime = time.time()
        print ("Running time: " + str(int(round(endtime * 1000)) - int(round(starttime * 1000))) + "ms")