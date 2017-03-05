import time
from operator import itemgetter #, attrgetter

start_time = time.time()
print ("Opening PDBCull file...")
PDBCULL = open("../../Datasets/PDBCull/cullpdb_pc20_res1.6_R0.25_d170302_chains3103.txt", 'r+')
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
    if (frval <= (rfact*1.05)) and (frval >= (rfact*0.95)): ##5% deviation from Rfactor
        PDBid.append(eachline[0])
        plength.append(int(eachline[1]))
        resolution.append(float(eachline[3]))
        R_factor.append(float(eachline[-2]))
        FreeRVal.append(float(eachline[-1]))
        ratio.append(round(float(eachline[-1])/float(eachline[-2]),8))

combined = list(zip(PDBid, plength, resolution, R_factor, FreeRVal, ratio))

print ("Sorting based on resolution, free R-value and R-factor...")
PDB = sorted(combined, key=itemgetter(2,5,3))

PDBsorted = []
PDBsor_del = []


count = 50
for i in PDB:
    temp_id = list(i[0])
    merged = ''.join(temp_id[:4])
    if merged not in PDBsorted:
        PDBsorted.append(merged)
        PDBsor_del.append(''.join(temp_id))
    if len(PDBsorted) == 50:
        break

PDBobtain_lower = []
for pdb in PDBsorted:
    PDBobtain_lower.append(pdb.lower())
PDBobtain_upper = []
for pdb in PDBsorted:
    PDBobtain_upper.append(pdb)

print ("Writing PDB entry IDs...")
with open("../../Datasets/PDBCull/PDB_Obtain_upper.txt", 'w+') as pou:
    for i in PDBobtain_upper:
        pou.write(i+'\n')

with open("../../Datasets/PDBCull/PDB_Obtain_lower.txt", 'w+') as pol:
    for i in PDBobtain_lower:
        pol.write(i+'\n')

with open("../../Datasets/PDBCull/PDB_Unmod.txt", 'w+') as pdu:
    for i in PDBsor_del:
        pdu.write(str(i)+'\n')


print ("Job finished in %rs." % (time.time() - start_time))
