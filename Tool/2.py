u = []
with open("../Data/SDB4.txt", "r") as l:
   for s in l.readlines():
        for i in s:
            if i not in u:
                u.append(i)
print(u)