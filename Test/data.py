with open("Online.txt", "r") as f:
    data=[]
    item=[]
    time0="08"
    user0="17850"
    seq = ""
    sdb = []
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
        dataitem=dataitem.split(' ',1)[1]
        item.append(dataitem)  #item是一条（08:26	17850   21730）数据
    for i in item:
        time = i[:2]
        user = i[6:11]
        if(time == time0):
            if(user == user0):
                code = i.split('\t', 2)[2][:1]
                if code<='9' and code>='0':
                    seq = seq+i.split('\t', 2)[2][:5]+" "
            else:
                seq = seq+"-1 "
                user0 = i.split('\t', 2)[1]
                code = i.split('\t', 2)[2][:1]
                if code <= '9' and code >= '0':
                    seq = seq + i.split('\t', 2)[2][:5] + " "
            #print(seq)

        else:
            sdb.append(seq)
            seq = ""
            time0 = i.split('\t', 2)[0][:2]
            user0 = i.split('\t', 2)[1]
            code = i.split('\t', 2)[2][:1]
            if code <= '9' and code >= '0':
                seq = seq + i.split('\t', 2)[2][:5] + " "
    with open("../Data/online-utility.txt", "w") as l:
        for sdb in sdb:
            l.write(sdb+'\n')
