import sys
from Bio.PDB.DSSP import make_dssp_dict as mdd
from Bio.PDB import PDBParser

#############################################################################
### RUN THIS THIRD
#############################################################################

PDB_original = []

PDB_lower = []

with open("../Temp/PDB_Original.txt", 'r') as po:
    po = po.read().splitlines()
    for i in po:
        PDB_original.append(i)

with open("../Temp/PDB_Obtain_lower.txt", 'r') as pl:
    pl = pl.read().splitlines()
    for i in pl:
        PDB_lower.append(i)

# PDB_original_low = set([i.lower() for i in PDB_original])
# print (len(PDB_original))

# PDB_lower = set(PDB_lower)
# print (len(PDB_lower))

print ("Acquiring sequences...\n")
proteinid, proteinseq = [], []
string = ''
with open("../Temp/master.fasta", 'r') as mf:
    mf = mf.read().splitlines()
    for stuff in PDB_original:
        proteinid.append('>'+stuff)
        for i,line in enumerate(mf):
            if stuff== line[1:7].replace(':',''):
                ID = True
                j = i+1
                while ID == True:
                    string = string + mf[j]
                    j=j+1
                    if j == len(mf):
                        break
                    if mf[j].startswith('>'):
                        ID = False
                proteinseq.append(string)
                string = ''
                continue
# print (proteinid)
zipped = list(zip(proteinid,proteinseq))
# print (len(proteinid), len(proteinseq))
path = "../Temp/Fasta/Process/"
for i in range(len(proteinid)):
    # print ("Writing %r" %proteinid[i])
    with open((path+proteinid[i]+'.fasta'), 'w+') as write:
        write.write(proteinid[i]+'\n'+proteinseq[i]+'\n')

###############################################################
### Checking for Non-standard amino acids
###############################################################
new_protid = []
new_protseq = []
nonstdAA = {'B','J','X','Z', 'U', 'O'}
print ("Checking proteins for non-standard amino acids...")
for i in range(0, len(zipped)):
    checkset = set(zipped[i][1])
    if any(i in checkset for i in nonstdAA) == False:
        new_protid.append(zipped[i][0])
        new_protseq.append(zipped[i][1])
    elif any(i in checkset for i in nonstdAA) == True:
        print ("Protein %s contains non-standard AA." %(zipped[i][0]))

###############################################################
### Writing the top 50 without nnstdAA into a file for psi-blast
###############################################################
zipped = list(zip(new_protid, new_protseq))
zipdel = list(zip(new_protid, new_protseq))

###############################################################
### Checking DSSP files
###############################################################
newzipdel = []
for i in range(len(zipdel)):
    newzipdel.append(zipdel[i][0])

classnames = ['(C) Coil', '(H) Helix', '(E) Sheets']
ss_map = {  'C':1, 'S':1, 'T':1,
            'H':2, 'G':2, 'I':2,
            'E':3, 'B':3} ## ALL '-' is treated as Coil
str_dict = {}
structures = ['H','G','I','E','B','S','T','C']
str_dict_untranslated = {}
print ("\nChecking DSSP files...\n")
for i in range(len(newzipdel)):
    filename = str(newzipdel[i][1:5]).lower()
    if filename not in PDB_lower:
        continue
    with open("../Temp/DSSP/"+filename+".dssp", 'r') as dssp:
        DSSP = dssp.read().splitlines()
        for lino in range(len(DSSP)):
            if DSSP[lino].startswith('  #'):
                thenumber = lino
        del DSSP[:(thenumber)]
        chainid = newzipdel[i][-1] ##CHAIN ID
        structurelist = [] #then check condition chainid
        structurelist_untr = []
        for line in DSSP[1:]:
            line = line.split()
            if line[2] == chainid:
                if line[4] not in structures:
                    structurelist.append(1)
                    structurelist_untr.extend('C')
                else:
                    structurelist.append(ss_map[line[4]])
                    structurelist_untr.extend(line[4])
        str_dict[newzipdel[i][1:]]=structurelist
        # structurelist_untr = str(structurelist_untr)
        structurelist_untr = ''.join(structurelist_untr)
        str_dict_untranslated[newzipdel[i][1:]]=structurelist_untr

dictkeys = list(str_dict.keys())
fastapath = "../Temp/Fasta/Original/>"
countmismatch = 0
count = 0

print (len(dictkeys))
with open("../Temp/TestProteins.txt", 'w+') as tpd:
    pass
for i in dictkeys:
    with open((fastapath+(i)+'.fasta'), 'r') as o:
        sequence = []
        o = o.read().splitlines()
        for line in o:
            if not line.startswith('>'):
                length = len(line)
                sequence.append(line)
    if length != (len(str_dict[i])):
        countmismatch += 1
        print ("[%s] Inconsistent DSSP structure and PDB sequence length, skipping..." %i)
    elif length == len(str_dict[i]):
        count += 1
        with open("../Temp/TestProteins.txt", 'a+') as tpd:
            tpd.write('>'+i+'\n')
            tpd.write(str(sequence[0])+'\n')
            tpd.write(str(str_dict_untranslated[i])+'\n')

print ("Number of consistent protein files: %d." %count)
print ("DSSP processing finished.")
