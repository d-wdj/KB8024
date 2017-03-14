import os
import sys
import glob
import time
import math
import numpy as np
import statistics as stat
from sklearn.externals import joblib
### THE CLASSIFIERS ############################################################
from sklearn.ensemble import RandomForestClassifier as RFC
################################################################################
print ("---PSSM-SUBSTITUTION MATRIX-BASED PREDICTOR---")
print ("Loading model...")
clf = joblib.load('SM.pkl')
print ("Model acquired. Ready to predict.")

# SECTION 1: OPENING FILE AND APPENDING INTO LISTS
################################################################################
### Opens the file and appends each feature of the file into
### the appropriate lists.
################################################################################
user_input = open(sys.argv[1], 'r+')
work_input = user_input.read().splitlines()

newpath = '../Results/'
if not os.path.exists(newpath):
    os.makedirs(newpath)

countprot = 0
i_protname = [work_input[i] for i in range(0, len(work_input),2)]
i_proteinseq = [work_input[i] for i in range(1, len(work_input),2)]
for i in i_proteinseq:
    countprot += 1

user_input.close()
print ("Number of sequences: ",countprot)

### Check for non-standard amino acids #########################################
for eachsequence in range(0, len(i_proteinseq)):
    for AA in range(0, len(i_proteinseq[eachsequence])):
        eachresidue = i_proteinseq[eachsequence][AA]
        if (eachresidue == 'B') or (eachresidue == 'J') or (eachresidue == 'U') or (eachresidue == 'X') or (eachresidue == 'O') or (eachresidue == 'Z'):
            print ("Non-standard amino acid '%s' detected in sequence %s position %d. Quitting..."
                    %(eachresidue, i_protname[eachsequence], AA))
            import sys
            sys.exit()
################################################################################

inv_ss_map = {1:'C', 2:'H', 3:'E'}
pred = []
ws = 11
n = int(ws/2)
pad = [list(np.zeros(20))]

################################################################################
### Defining function for 'normalising' substitution matrix values
################################################################################
def sigmoid(x):
    return (1 / (1 + math.exp(-x)))

################################################################################
### Running psi-blast on input protein
################################################################################
for i in range(len(i_protname)):
    filepath = "../Temp/"
    with open((filepath+str(i_protname[i])+'.fasta'), 'w') as fasta:
        fasta.write(str(i_protname[i])+'\n')
        fasta.write(str(i_proteinseq[i])+'\n')

print ("Checking for PSI-BLAST PSSM files...")
Temp = '../Temp'
os.chdir(Temp)
for fastafile in glob.glob('*.fasta'):
    cmd = """#!/bin/bash
    export BLASTDB=/local_uniref/uniref/uniref90
    if [ ! -f "{fa}.pssm" ] ; then
    echo "Running PSI-BLAST on '{fa}' at $(date)..."
    psiblast -query '{fa}' -evalue 0.01 -db uniref90.db -num_iterations 3  -out '{fa}.psiblast' -out_ascii_pssm '{fa}.pssm' -num_threads 8 -comp_based_stats 0
    echo "Finished PSI-BLAST on '{fa}' at $(date).
    "
    fi

    """.format(fa=fastafile)
    os.system(cmd)
os.chdir("../bin")

################################################################################
### Collate the psi-blast PSSM profiles for each sequence.
################################################################################
print ("Processing PSI-BLAST PSSM file of your sequence(s)...")
pred = []
combined_SM = []
secondarystruc = []
count = 0
for i in range(len(i_protname)):
    count += 1
    protnamepath = ('../Temp/'+str(i_protname[i])+'.fasta.pssm')
    with open(protnamepath, 'r+') as PSSM:
        pssm = PSSM.read().splitlines()
        del pssm[0:3]
        del pssm[-6:]
        substitutionmatrix = [] #2-22
        for everyline in pssm:
            pssm_split = everyline.split()
            tmp_sm = pssm_split[2:22]
            tmp_sm2 = []
            for SM in tmp_sm:
                tmp_sm2.append(sigmoid(float(SM)))
            substitutionmatrix.append(tmp_sm2)
        combined_SM.append(substitutionmatrix)
    for protseq in combined_SM:
        countless = 0
        countmore = 0
        countrest = 0
        SM_Windows = []
        for i in range(0, len(protseq)):
            if i < n:
                window = (pad*(n-i)) + protseq[0:ws-(n-i)]
                window = [j for i in window for j in i]
                SM_Windows.append(window)
                countless += 1
            elif i >= (len(protseq)-n):
                addprot = protseq[(i-n):ws-(n-i)+1]
                if len(addprot) != ws:
                    addprot.extend(pad*(ws-len(addprot)))
                addprot = [j for i in addprot for j in i]
                countmore += 1
                SM_Windows.append(addprot)
            else:
                window = protseq[(i-n):(i+n+1)]
                window = [j for i in window for j in i]
                SM_Windows.append(window)
                countrest += 1
        total = countless + countmore + countrest
        if len(protseq) != total:
            print ("Something is wrong with the trainset window slicing. Quitting...")
            import sys
            sys.exit()
        print ("Predicting sequence %d/%d..." %(count, countprot))
        prediction = list(clf.predict(SM_Windows))
        prediction = [inv_ss_map[i] for i in prediction]
        prediction = ''.join(prediction)
        if (sys.argv[3] == 'y') or (sys.argv[3] == 'Y'):
            print (i_protname[countprot-1])
            print (prediction)
        pred.append(prediction)
################################################################################

print ("Writing prediction output into %s..." %(newpath+'SM_'+sys.argv[2]))
runtime = time.strftime("%Y-%m-%d %H:%M %Z")
with open((newpath+'SM_'+sys.argv[2]), 'w+') as op:
    op.write("HSCPred PSSM-Substitution matrix-based prediction "+runtime+'\n')
    for i in range(0, len(i_protname)):
        op.write(str(i_protname[i])+'\n')
        op.write(str(i_proteinseq[i])+'\n')
        op.write(str(pred[i])+'\n')
    op.write("Generated using HSCPred -- (C)2017 - Dimitri Wirjowerdojo ")

print ("\nHSC Prediction finished. Have a good day!\n")
