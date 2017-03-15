import sys
import statistics as stat
SEQUENCE = open('../Temp/TestProteins.txt', 'r+')
Sequence = SEQUENCE.read().splitlines()
print ("Opening the files and appending data features into their lists...")
protname = []
proteinseq = []
secondstruc = []
countprot = 0
for i in range(0, len(Sequence), 3):
    protname.append(Sequence[i].lstrip('>'))
for i in range(1, len(Sequence), 3):
    proteinseq.append(Sequence[i])
    countprot += 1
for i in range(2, len(Sequence), 3):
    secondstruc.append(Sequence[i])
SEQUENCE.close()
print ("Number of sequences: ",countprot)

C_counter = []
H_counter = []
S_counter = []

for easeq in secondstruc:
    totallen = len(easeq)
    countC = 0
    countH = 0
    countS = 0
    for eass in easeq:
        if eass == 'C':
            countC += 1
        elif eass == 'H':
            countH += 1
        else:
            countS += 1
    Cper = round((float(countC/totallen)*100),2)
    C_counter.append(Cper)
    Hper = round((float(countH/totallen)*100),2)
    H_counter.append(Hper)
    Sper = round((float(countS/totallen)*100),2)
    S_counter.append(Sper)

zipped=list(zip(protname,C_counter,H_counter,S_counter))


newlist = []
countless = 0
for i in range(len(zipped)):
    # zipped.append(zipped[i])
    if (zipped[i][3] < 80) and (zipped[i][3] > 15):# and (zipped[i][3] > 20):# and (20 > zipped[i][2] < 95) and (20 > zipped[i][1] < 95):
        if (zipped[i][1] > 15):
            if (zipped[i][2] > 15):
                newlist.append(zipped[i])
                countless += 1
for i in range(len(newlist)):
    print (newlist[i])
print ("Total number of filtered sequences: %d." %countless)

C_counter = [newlist[i][1] for i in range(len(newlist))]
H_counter = [newlist[i][2] for i in range(len(newlist))]
S_counter = [newlist[i][3] for i in range(len(newlist))]

# print (len(newlist), len(newlist))
# sys.exit()
C_counter_1 = stat.mean(C_counter)
C_counter_err = stat.stdev(C_counter)

H_counter_1 = stat.mean(H_counter)
H_counter_err = stat.stdev(H_counter)

S_counter_1 = stat.mean(S_counter)
S_counter_err = stat.stdev(S_counter)

a = "Average Coil content percentage: %2.2f +/- %2.2f." %(C_counter_1, C_counter_err)
b = "Average Helix content percentage: %2.2f +/- %2.2f." %(H_counter_1, H_counter_err)
c = "Average Sheet content percentage: %2.2f +/- %2.2f." %(S_counter_1, S_counter_err)

print(a)
print(b)
print(c)
with open("../Temp/HSC Content TestSet.txt", 'w+') as hsc:
    hsc.write(a+'\n')
    hsc.write(b+'\n')
    hsc.write(c+'\n')


# newlist=list(zip(protname,C_counter,H_counter,S_counter))
del newlist[50:]
print ("Number of sequences after deletion: %d." %(len(newlist)))
for i in range(len(newlist)):
    print (newlist[i])

with open("../Temp/HSC Content TestSet.txt", 'a+') as hsc:
    hsc.write('PDBID C(%) H(%) S(%)\n')
    for i in range(0,len(newlist)):
        hsc.write('>'+str(newlist[i][0])+'    C:'+str(newlist[i][1])+'   H:'+str(newlist[i][2])+'   S:'+str(newlist[i][3])+'\n')
with open("../Temp/Fasta/ForPSIBLAST.txt", 'w+') as hsc:
    for i in range(0,len(newlist)):
        hsc.write('>'+str(newlist[i][0])+'\n')

print ("HSC Counter finished.")
