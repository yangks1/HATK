import copy
import time


'''
读取文件
'''
def read_file():
    # addr_file = 'files/Italian-tem.txt'
    # addr_file = 'files/PRSA_Data_Nongzhanguan.txt'
    addr_file = 'files/Italian-temperature.txt'
    with open(addr_file, 'r') as f:
        lines = f.readlines()
    global obj_s
    temp = list(filter(lambda x: x.strip(), lines))
    obj_s = list(map(lambda x: float(x.strip('\n')), temp))

'''
验证幅值(幅值小的匹配忽略)
'''
def verify_amplitude():
    # 1.过滤幅值小的点（当前点分别与前一个点和后一个点的绝对值小于某值）
    # 2.如果是幅值小的点，则保留3者中最小的点其他2个点删除
    pass

'''
验证一次性
'''
def verify_one_off():
    pass

'''
    最初长度为2的模式
'''
def init_pattern():
    emerge = list()
    emerge2 = list()
    for i in range(len(obj_s)-1):
        if obj_s[i+1] > obj_s[i]:
            emerge.append(i+1)
        elif obj_s[i+1] < obj_s[i]:
            emerge2.append(i+1)
    judge_fre([1,2],emerge)
    judge_fre([2,1],emerge2)

'''
    频繁模式挖掘
'''
def judge_fre(cand, emerge):
    global minsup, candList, emergeList, frequent_num, fre_num
    if len(emerge) >= minsup:
        candList.append(cand)
        emergeList.append(emerge)
        fre_num = fre_num + 1
        frequent_num = frequent_num + 1

'''
    生成保序序列模式
'''
def order_preserving_generate(src_seq):
    array_sort = [0 for _ in range(len(src_seq))]
    seq_sort = sorted(src_seq)
    for i, v in enumerate(src_seq):
        array_sort[i] = seq_sort.index(v) + 1
    return array_sort


'''
    候选模式_模式融合
'''
def generate_fre():
    global minsup, candList, emergeList, frequent_num, fre_num, cand_num
    # 模式长度
    seq_len = len(candList[0])
    freList = copy.deepcopy(candList)
    candList.clear()
    fre_number = fre_num
    fre_num = 0
    posList = copy.deepcopy(emergeList)
    emergeList.clear()

    for i in range(fre_number):
        # 后缀
        sufPa = freList[i][1:seq_len]
        # 后缀保序
        sufPaOrder = order_preserving_generate(sufPa)

        for j in range(fre_number):
            cand_r = [0 for _ in range(seq_len+1)]
            cand_h = [0 for _ in range(seq_len+1)]
            # 前缀
            prePa = freList[j][:seq_len - 1]
            # 保序前缀
            prePaOrder = order_preserving_generate(prePa)
            if sufPaOrder == prePaOrder:
                # 最前最后位置相等，拼接成两个模式
                if freList[i][0] == freList[j][seq_len - 1]:
                    cand_r[0] = freList[i][0]
                    cand_h[0] = freList[i][0] + 1
                    cand_r[seq_len] = freList[i][0] + 1
                    cand_h[seq_len] = freList[i][0]
                    for t in range(1, seq_len):
                        # 中间位置增长
                        if freList[i][t] > freList[j][seq_len - 1]:
                            cand_r[t] = freList[i][t] + 1
                            cand_h[t] = freList[i][t] + 1
                        else:
                            cand_r[t] = freList[i][t]
                            cand_h[t] = freList[i][t]
                    cand_num = cand_num + 2
                    # print('1111111111')
                    # print(cand_r,cand_h)
                    grow_basep2(posList[i], posList[j], cand_r, cand_h)
                #     第一个位置比最后一个位置小
                elif freList[i][0] < freList[j][seq_len - 1]:
                    # 小值不变
                    cand_r[0] = freList[i][0]
                    # 大值加一
                    cand_r[seq_len] = freList[j][seq_len - 1] + 1
                    for t in range(1, seq_len):
                        # 中间位置增长
                        if freList[i][t] > freList[j][seq_len - 1]:
                            cand_r[t] = freList[i][t] + 1
                        else:
                            cand_r[t] = freList[i][t]
                    cand_num = cand_num + 1
                    # print('2222222220')
                    # print(cand_r)
                    grow_basep1(posList[i], posList[j], cand_r)
                #     第一个位置比最后一个位置大
                else:
                    # 大值加一
                    cand_r[0] = freList[i][0] + 1
                    # 小值不变
                    cand_r[seq_len] = freList[j][seq_len - 1]
                    for t in range(seq_len - 1):
                        # 中间位置增长
                        if freList[j][t] > freList[i][0]:
                            cand_r[t + 1] = freList[j][t] + 1
                        else:
                            cand_r[t + 1] = freList[j][t]
                    cand_num = cand_num + 1
                    # print('33333333')
                    # print(cand_r)
                    grow_basep1(posList[i], posList[j], cand_r)


'''支持度计算（方法一）'''
def grow_basep1(preList, posList, cand_r):
    emerge = list()
    k = 0
    for i in preList:
        for j in range(k, len(posList)):
            if i+1 == posList[j]:
                emerge.append(posList[j])
                k = j+1
                break
            elif i < posList[j]:
                break
            else:
                continue
    judge_fre(cand_r, emerge)

'''支持度计算（方法二）'''
def grow_basep2(preList, posList, cand_r, cand_h):
    emerge = list()
    emerge2 = list()
    len_cand = len(cand_r)-1
    k = 0
    for i in preList:
        for j in range(k, len(posList)):
            if i+1 == posList[j]:
                lst = posList[j]
                fri = lst - len_cand
                if obj_s[lst] > obj_s[fri]:
                    emerge.append(lst)
                elif obj_s[lst] < obj_s[fri]:
                    emerge2.append(lst)
                k = j+1
                break
            elif i < posList[j]:
                break
            else:
                continue

    judge_fre(cand_r, emerge)
    judge_fre(cand_h, emerge2)

# 时间序列
obj_s = list()
# 候选模式列表
candList = list()
# 模式出现列表
emergeList = list()
# 最小支持度
minsup = 12
# 总频繁模式数量
frequent_num = 0
fre_num = 0
# 候选模式数量
cand_num = 2

if __name__ == '__main__':
    read_file()
    starttime = time.time()
    init_pattern()
    while fre_num:
        generate_fre()
    endtime = time.time()

    print(int(round(endtime * 1000)) - int(round(starttime * 1000)))
    print(frequent_num)
    print(cand_num)
