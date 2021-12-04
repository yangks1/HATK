from decimal import Decimal

with open("utiltyTable.txt", "r") as f:
    data = []
    item = []
    code0 = "10002"
    unitPrice0 = 0.85
    seq = ""
    sdb = []
    tag = 0
    # 对文件f中的数据处理存入data列表中
    for line in f.readlines():
        # Python strip ()方法用于移除字符串头尾指定的字符（默认为空格）。
        # 去掉每行头尾换行
        line = line.strip('\n')
        # 加入列表data中
        data.append(line)
    # 对列表data中的数据处理存入列表item中
    for dataitem in data:
        # dataitem是一条(2010-12-1 08:26	17850	21730)数据
        # Python split() 通过指定分隔符对字符串进行切片，如果参数 num 有指定值，则分隔 num+1 个子字符串
        # 返回分割后的字符串列表
        #     -------只存入编号第一个符号是数字并只取前五个字符
        str1 = dataitem.split('\t', 4)[0][0:5]
        if str1[:1] >= '0' and str1[:1] <= '9':
            dataitem = dataitem.split('\t', 4)[0][:5] + '\t' + dataitem.split('\t', 4)[4]
            item.append(dataitem)  # item是一条（17850   0.85）数据

    for i in item:
        code = i.split('\t', 1)[0]
        unitPrice = float(i.split('\t', 1)[1])
        if unitPrice != 0.0:
            if (code == code0):
               tag = tag + 1
               unitPrice0 = unitPrice0 + unitPrice
            else:
                seq = seq + code0
                unitPrice0 = unitPrice0 / tag
                unitPrice0 = '%.2f' %unitPrice0
                seq = seq + '\t' + unitPrice0
                sdb.append(seq)
                seq = ""
                code0 = code
                unitPrice0 = unitPrice
                tag = 1
    seq = seq + code0
    unitPrice0 = unitPrice0 / tag
    unitPrice0 = '%.2f' % unitPrice0
    seq = seq + '\t' + str(unitPrice0)
    sdb.append(seq)
    seq = ""
    code0 = code
    unitPrice0 = unitPrice
    tag = 0
    with open("1.txt", "w") as l:
        for sdb in sdb:
            l.write(sdb + '\n')
