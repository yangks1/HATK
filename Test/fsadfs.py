
if __name__ == '__main__':
    n = int(input("请输入线段条数："))
    strnum = []
    for i in range(0, n):
        str = raw_input()
        strnum.append(str)
    num = []
    mar = 0
    for s in strnum:
        temp = s.split(",")
        n1 = temp[0]
        n2 = temp[1]
        if n2 > mar:
            for i in range(0, n2 - mar):
                num.append(0)
        for i in range(n1, n2):
            num[i] += 1
    # for i in num:
    #



