fn = [["../Data/chainstore.txt", "../Data/chainstoreUtility.txt"],
      ["../Data/MicroblogPCU.txt", "../Data/MicroblogPCUUtility.txt"],
      ["../Data/Online-2.txt", "../Data/Online2Utility.txt"],
      ["../Data/online-utility.txt", "../Data/onlineUtilityTable.txt"],
      ["../Data/Sds1.txt", "../Data/Sds1-utility.txt"],
      ["../Data/Sds2.txt", "../Data/Sds2-utility.txt"],
      ["../Data/Sds3.txt", "../Data/Sds3-utility.txt"],
      ["../Data/Sds4.txt", "../Data/Sds4-utility.txt"],
      ["../Data/creatData1.txt", "../Data/creatDataUtility1.txt"],
      ["../Data/creatData2.txt", "../Data/creatDataUtility2.txt"],
      ["../Data/creatData3.txt", "../Data/creatDataUtility3.txt"],
      ["../Data/creatData4.txt", "../Data/creatDataUtility4.txt"]]
for i in fn:
    t = i[0]
    i[0] = i[1]
    i[1] = t
print(fn)
fn = [['../Data/chainstoreUtility.txt', '../Data/chainstore.txt'],
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
