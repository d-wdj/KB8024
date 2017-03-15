import sys
import time
from operator import itemgetter #, attrgetter
from sklearn.utils import shuffle

#############################################################################
### RUN THIS FIRST
#############################################################################

start_time = time.time()
print ("Opening PDBCull file...")

def PDBCull(filename):
    PDBCULL = open(filename, 'r+')
    pdbcull = PDBCULL.read().splitlines()

    PDBid = []
    plength = []
    resolution = []
    R_factor = []
    FreeRVal = []
    ratio = [] ##freeRval/Rfactor, the closest to 1 the better

    print ("Extracting information...")
    for line in range(1, len(pdbcull)):
        eachline = pdbcull[line].split()
        frval = float(eachline[-1])
        rfact = float(eachline[-2])
        if (frval <= (rfact*1.1)) and (frval >= (rfact*0.9)): ##5% deviation from Rfactor
            PDBid.append(eachline[0])
            plength.append(int(eachline[1]))
            resolution.append(float(eachline[3]))
            R_factor.append(float(eachline[-2]))
            FreeRVal.append(float(eachline[-1]))
            ratio.append(round(float(eachline[-1])/float(eachline[-2]),8))

    combined = list(zip(PDBid, plength, resolution, R_factor, FreeRVal, ratio))

    print ("Sorting based on resolution, free R-value and R-factor...")
    PDB = sorted(combined, key=itemgetter(2,5,3))
    # print (PDB[:5])
    # PDB = shuffle(PDB)
    # print (PDB[:5])



    PDBsorted = []
    PDBsor_del = []


    # count = 50
    for i in PDB:
        temp_id = list(i[0])
        if temp_id not in PDBsor_del:
            a = ''.join(temp_id)
            PDBsor_del.append(a)
            del temp_id[-1]
            b = ''.join(temp_id)
            if b not in PDBsorted:
                PDBsorted.append(b)
            # if len(PDBsor_del) == 50:
            #     break

        # del temp_id[-1]
        # temp_id = ''.join(temp_id)
        # if temp_id not in PDBsorted:
        #     PDBsorted.append(temp_id)
        # if len(PDBsorted) == 50:
        #     break

    PDBobtain_lower = []
    PDBobtain_upper = []
    for pdb in PDBsorted:
        PDBobtain_lower.append(pdb.lower())
        PDBobtain_upper.append(pdb)


    print ("Writing PDB entry IDs...")
    with open("../Temp/PDB_Obtain_upper.txt", 'w+') as pou:
        for i in PDBobtain_upper:
            pou.write(i+'\n')

    with open("../Temp/PDB_Obtain_lower.txt", 'w+') as pol:
        for i in PDBobtain_lower:
            pol.write(i+'\n')

    with open("../Temp/PDB_Original.txt", 'w+') as pol:
        for i in PDBsor_del:
            pol.write(i+'\n')



print ("""PDB Cull parameters: (PC) Sequence similarity; (Res) Resolution; (R) R-factor.
[0] PC5     Res1.6    R0.3
[1] PC20    Res1.6    R0.25
[2] PC20    Res2.0    R0.25""")

no0 = "../cullpdb_pc5_res1.6_R0.3_d170312_chains1720.txt"
no1 = "../cullpdb_pc20_res1.6_R0.25_d170302_chains3103.txt"
no2 = "../cullpdb_pc20_res2.0_R0.25_d170309_chains6368.txt"

while True:
    option = int(input("PDBCull file selection: "))
    if option == 0:
        PDBCull(no0)
        break
    if option == 1:
        PDBCull(no1)
        break
    if option == 2:
        PDBCull(no2)
        break

print ("PDBCull extraction finished in %0.2f seconds." %(time.time()-start_time))
