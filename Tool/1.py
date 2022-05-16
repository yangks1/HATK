if __name__ == '__main__':
    s1 = [["1", "2", "3"], ["1", "2", "3"], ["1", "2", "3"]]
    p = [["1", "3"], ["3"]]
    s = []
    for ss in s1:
        s.append(ss[:])
    occnum = 0
    i = 0
    while i < len(s):
        position = []
        j = 0
        while j < len(p) and i < len(s):
            if set(p[j]).issubset(set(s[i])):
                for k in p[j]:
                    s[i].remove(k)
                position.append(i)
                j += 1
                i += 1

            else:
                i += 1
        if j == len(p):
            occnum += 1
            i = position[0] + 1
        else:
            break
    print(occnum)
    print(s1)
