import re
import time
from Tool import Pdata

pdata = Pdata.processingData()

# 读取文件
# return lines_s=[S1,S2,S3,...]
def read_file(readfilename):
    # 读取的文件名字
    # readFileName = "../dateset/demo.txt"
    lines_s = []
    with open(readfilename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            lines_s.append(line.strip())
    return lines_s   # 返回数组

#项集去重 排序
# sort_items  去重排序后的项集数组
# items_no_repeat  存在重复的未排序的项集数组
def item_sotrd(items):
    items_no_repeat = []
    for item in items:
        if item not in items_no_repeat :
            items_no_repeat.append(item)
    write_file(items_no_repeat,'item_norepeat.txt')
    sort_items = list(sorted(items_no_repeat))
    # 去重排序后的项集
    # print_array (sort_date)
    # print(type(sort_date))
    return sort_items,items_no_repeat

#定义空的数据字典
'''
S =
{
'0': {'all': [[], [], [], []], 'mul': [[], [], [], []]},
'1': {'all': [[], [], [], []], 'mul': [[], [], [], []]},
'2': {'all': [[], [], [], []], 'mul': [[], [], [], []]},
'3': {'all': [[], [], [], []], 'mul': [[], [], [], []]},
'4': {'all': [[], [], [], []], 'mul': [[], [], [], []]},
'5': {'all': [[], [], [], []], 'mul': [[], [], [], []]},
'6': {'all': [[], [], [], []], 'mul': [[], [], [], []]},
'7': {'all': [[], [], [], []], 'mul': [[], [], [], []]},
}
'''
def item_to_dict(sort_items,len_lines):
    # sort_items 排序去重之后的项
    # len_lines 序列数
    S={}
    for i in range(len(sort_items)):
        S[str(i)]={}
        S[str(i)]['all']=[[] for i in range(len_lines)]
        S[str(i)]['mul']=[[] for i in range(len_lines)]
    # print (S)
    return S

# 替换字符串为项集(按字符串的大小)
def replace_seq(lines_s,sort_item):
    # print(sort_item)
    # print(lines_s)
    flag = 1
    for i in range(len(sort_item)):
        for j in range(len(lines_s)):
            if flag==1:
                lines_s[j] = lines_s[j] + " "
            # lines_s[j] = lines_s[j].replace(sort_item[i], str(i))
            p1= re.compile(" "+sort_item[i]+" ")
            lines_s[j],number= re.subn(p1, " "+str(i)+"* ", lines_s[j])
        # print(lines_s)
        # print(number)
    # print_array(lines_s)
        flag = 0
    for i in range(len(lines_s)):
        lines_s[i] = lines_s[i].replace('*', '')
    return lines_s

#分割字符串数组返回[]和[[],[],[]]
def split_array(lines):
    # lines =  0 2 -1 0 2 -1 2 -1 0 2 -1 2
    lines = lines.replace('  ',' ')
    # print(lines)
    items_array= lines.strip().split(' ') # 按空格分隔成一个一个的项和-1
    print(items_array)
    s_array=[[]]  #二维数组
    i = 0
    for item in items_array:
        if item != '-1':
            s_array[i].append(item)
        else:
            i=i+1
            s_array.append([])
    print(s_array)
    return items_array,s_array
#  lines  0 2 -1 0 2 -1 2 -1 0 2 -1 2
#  items_array  ['0', '2', '-1', '0', '2', '-1', '2', '-1', '0', '2', '-1', '2']
#  s_array  [['0', '2'], ['0', '2'], ['2'], ['0', '2'], ['2']]

def Statistics_items(lines,items):
    # lines =  "177 179 410 454 468 470 474 475 513 588 871 872 873 1142 1011 1107  -1 854 854 854  -1 730 761 859 861 864 870 918 919 927  -1 436 1199  -1 859  -1 919  -1 70 153 217 235 255 256 283 318 360 361 376 436 464 464 693 736 736 736 737 751 775 776 777 800 801 871 872 881 888 900 910 916 940 1039 1094 1116  -1 139 262 301 325 452 477 497 711 1034 1097 1099 1179 1107 1154  -1 119 120 121 548 642 691 776 817 837 848 910 911 912 917 919 966 1099 966B  -1 248 362 427 451 460 470 494 495 588 594 595 659 660 662 663 664 665 666 667 679 680 691 691 692 693 694 695 696 699 704 708 708 708 761 775 776 777 778 799 840 841 871 872 873 887 888 909 912 1088 1095 1135  -1 17 43 118 119 190 269 453 529 633 708 708 708 736 784 785 787 826 826 833 863 887 908 920 1096 1096 1011 1011 1041 1055 1055 1060 1130 1157  -1 307 308 715 716 718 819  -1 301 489 1154  -1 34 152 191 238 309 371 471 612 634 635 684 750 759 827 977 1026 1028 1097 1098 1163 975 1030  -1 44 90 104 319 338 373 555 585 634 661 662 665 666 666 667 675 749 1179 13 1062 1107"
    lines = lines.replace('  ',' ') # 将两个空格替换成一个空格 所有项之间都保持一个空格
    items_array= lines.strip().split(' ') # 按空格分隔序列 收集所有的项 包含重复
    for item in items_array:
        if item != '-1' and item not in items: # 如果项不是项集分隔符并且没有在items中重复就将项保存在items
            items.append(item)
    # print_array(items)
    return items # 返回不重复的项的集合(无序的 按照在序列中出现先后的顺序)

#生成数据字典格式
def General_Sn(lines_s,S,sort_item):
    #数据处理后的最终结果
    itemcount = 0
    for i in range(len(lines_s)):
        # print(lines_s)
        items_array,s_array = split_array(lines_s[i])
        for j in s_array:
            itemcount += len(j)
        #  lines_s[i]  0 2 -1 0 2 -1 2 -1 0 2 -1 2
        #  items_array  ['0', '2', '-1', '0', '2', '-1', '2', '-1', '0', '2', '-1', '2']
        #  s_array  [['0', '2'], ['0', '2'], ['2'], ['0', '2'], ['2']]
        sort_item, items_no_repeat = item_sotrd(items_array)
        # sort_item 第i条序列去重排序之后的项 ['-1', '0', '2']
        # print(sort_item)
        for item in sort_item:
            if item != '-1':
                for k in range(len(s_array)):
                    if item in s_array[k]:
                        # index = str(sort_item.index(item))
                        # print(item)
                        # print(i)
                        # print(k)
                        # print('$$$$$$$$$$$$$$$')
                        S[item]['all'][i].append(k)
                        if len(s_array[k])>1:
                            S[item]['mul'][i].append(k)
    print(itemcount)
    return S

def Min_FP(SeqNum,S,sort_item):
    # lines_s 替换后的序列 用于获取序列数
    # S 项的出现位置字典 用于计算支持度
    # sort_item 去重排序后的项 用于生成模式 注意：此项未进行替换
    P = {}  #存储模式的出现位置
    LP = {} #存储模式的项集子模式的出现位置
    FP = [] #存储频繁模式
    FP1=[]  #存储长度为1的频繁模式 用于模式增长
    minsup = 100000
    CanNum = 0
    # SeqNum = len(lines_s)
    '''
    P 用于存储模式的最后位置
    P =
    {
        '0': [[], [], [], []],
        '1': [[], [], [], []],
        '2': [[], [], [], []],
        '3': [[], [], [], []],
        '4': [[], [], [], []],
        '0 -1 0': [[], [], [], []],
        '0 1': [[], [], [], []]
        ......
    }
    '''
    count = 0
    for i in range(len(sort_item)):
        CanNum += 1
        for j in range(SeqNum):
            # print (S)
            # print (S[str(i)]['all'][j])
            count += len(S[str(i)][j])
        # print (str(i)+":"+str(count)) #输出各项及其出现次数
        if count >= minsup:
            FP1.append(str(i))
            FP.append(str(i))
            P[str(i)] = [[] for k in range(SeqNum)]
            P[str(i)] = S[str(i)]
            # print(P)
            LP[str(i)] = [[] for k in range(SeqNum)]
            for k in range(SeqNum):
                for t in range(len(P[str(i)][k])):
                    LP[str(i)][k].append(P[str(i)][k][t] -1)
            # print(LP)
        count = 0
    # print (P)
    # print (LP)
    # print (FP1)
    # print (FP)
    flag = 0
    for fp in FP: # fp: str
        # print (fp)
        for item in FP1: # item: str
            # print (type(fp))
            # print (type(item))
            # print (item)
            pattern = fp + " -1 " + item # S连接**************************************
            CanNum += 1
            LP[str(i)] = [[] for k in range(SeqNum)]
            LP[pattern] = P[fp]
            P[pattern] = [[] for i in range(SeqNum)]
            # print (pattern)
            # for i in range(len(lines_s)):
            for i in range(SeqNum):
                # print(S[fp]['all'][i])
                # print(S[item]['all'][i])
                # print('*')
                for j in range(len(P[fp][i])):
                    for k in range(flag, len(S[item][i])):
                        if S[item][i][k] > P[fp][i][j]:
                            P[pattern][i].append(S[item][i][k])
                            count += 1
                            flag = k+1
                            break
                            # print (flag)
                flag = 0
            if count >= minsup:
                FP.append(pattern)
                # print (pattern + ': ', end = "")
                # print (P[pattern])
                # print ('count=' + str(count))
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
                # print (pattern)
                # unit = [[] for i in range(SeqNum)]
                #******************************************************
                unit = S[item][:]
                # print(item + str(unit))
                # print(unit)
                pattern_array = fp.strip().split(' ')
                f = -1
                for i in range(len(pattern_array)):
                    if pattern_array[i] == '-1':
                        f = i
                for i in range(f+1, len(pattern_array)):
                    for j in range(len(unit)):
                        # print("###############")
                        # print(unit[j])
                        # print(S[pattern_array[i]]['all'][j])
                        # print("################")
                        unit[j] = list(set(unit[j]) & set(S[pattern_array[i]][j]))
                        # print(unit[j])
                f = -1
                # print(unit)
                for i in range(SeqNum):
                    # print(S[fp]['all'][i])
                    # print(S[item]['all'][i])
                    # print('*')
                    for j in range(len(LP[fp][i])):
                        for k in range(flag, len(unit[i])):
                            if unit[i][k] > LP[fp][i][j]:
                                P[pattern][i].append(unit[i][k])
                                count += 1
                                flag = k + 1
                                break
                                # print (flag)
                    flag = 0
                # print(pattern + ': ', end="")
                # print(P[pattern])
                # print('count=' + str(count))
                # print("**********")
                #************************************
                # for i in range(SeqNum):
                #     for j in range(len(S[item]['all'][i])):
                #         if S[item]['all'][i][j] in P[fp][i]:
                #             P[pattern][i].append(S[item]['all'][i][j])
                #             count +=1
                # print(pattern + ': ', end="")
                # print(P[pattern])
                # print('count=' + str(count))
                # print("**********")
                if count >= minsup:
                    FP.append(pattern)
                    # print(pattern + ': ', end="")
                    # print(P[pattern])
                    # print('count=' + str(count))
                    # print("**********")
                else:
                    del P[pattern]
                    del LP[pattern]
            count = 0
        del P[fp]
        del LP[fp]
    print ("Frequent patterns:", end = " ")
    print (FP)
    print ("Number of frequent patterns: " + str(len(FP)))
    print ("Number of candidate patterns: " + str(CanNum))

#输出数组内容的函数
def print_array(items):
    for i in range(len(items)):
        print(str(i)+'\t'+items[i])

#将数组写入文件
def write_file(lines_s,filename):
     with open(filename, 'w') as f:
        for i in range(len(lines_s)):
            f.writelines(str(i)+"\t"+lines_s[i])
            f.write("\n")


if __name__ == '__main__':
    readFileName = "../dataset/demo/E-Shop.txt"
    S = {}
    SeqNum, S, sort_item = pdata.datap(readFileName, S)
    del pdata
    #数据处理后的最终结果
    # S={}
    # # 读取的文件名字
    # # readFileName = "../dataset/online-fin.txt"
    # readFileName = "../dataset/demo/MicroblogPCU.txt"
    # # 文件读取后的字符串数组 序列集合S
    # lines_s = read_file(readFileName)
    # # print(lines_s)
    #
    # # items 项集 统计后的项集(序列中出现的字符集 按照在序列中出现的次序)
    # items=[]
    # for lines in lines_s:
    #     items=Statistics_items(lines,items)
    # # print(items)
    #
    # # sort_item 排序后的项集字符串数组
    # # date_no_repeat 未排序的项 在序列中出现的次序
    # sort_item,items_no_repeat = item_sotrd(items)
    # #输出 sort_item
    # # print_array(sort_item)
    # # print_array(items_no_repeat)
    # #将sort_item数组写入文件sort_item.txt
    # write_file(sort_item,'sort_item.txt')
    # #
    # #替换数据集中的字符串lines_s 替换后的字符串数组
    # # print(lines_s)
    # lines_s = replace_seq(lines_s,sort_item)
    # # print(lines_s)
    # write_file(lines_s,"demo2.txt")
    # # print(lines_s)
    # # print_array(lines_s)
    # # print(len(lines_s))
    # S = item_to_dict(sort_item,len(lines_s)) # 排序后的项 和 序列数
    # print(lines_s)
    # S = General_Sn(lines_s,S,sort_item) # 根据sort_item替换后的序列 空的字典 排序后的项
    # # 输出字典数据集
    # json_str = json.dumps(S)
    # with open('test_data.json', 'w') as json_file:
    #     json_file.write(json_str)
    # print(S)
    # 字典格式化输出
    # print (json.dumps(S,indent=4))
    #
    starttime = time.time()
    Min_FP(SeqNum, S, sort_item) # lines_s:替换后的序列 S:位置字典 sort_item:字符集
    endtime = time.time()
    print ("Running time: " + str(int(round(endtime * 1000)) - int(round(starttime * 1000))) + "ms")
    # print ("Running time: " + str(int(round(endtime)) - int(round(starttime))) + "s")