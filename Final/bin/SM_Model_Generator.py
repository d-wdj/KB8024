import time
import math
import itertools
import numpy as np
import statistics as stat
from sklearn.utils import shuffle
from sklearn.externals import joblib
### THE CLASSIFIERS ############################################################
from sklearn.ensemble import RandomForestClassifier as RFC
################################################################################

# SECTION 1: OPENING FILE AND APPENDING INTO LISTS
################################################################################
### Opens the file and appends each feature of the file into
### the appropriate lists.
################################################################################
SEQUENCE = open('../Datasets/dssp_3state.3line.txt', 'r+')
Sequence = SEQUENCE.read().splitlines()
start = time.time()
protname = []
proteinseq = []
secondstruc = []
countprot = 0
testcount = 399 ### CHANGE NUMBER HERE TO PLAY WITH NUMBER OF PROTEINS TESTED, MAX 399
for i in range(0, len(Sequence), 3):
    protname.append(Sequence[i].lstrip('>'))
    if len(protname) == testcount:
        break
for i in range(1, len(Sequence), 3):
    proteinseq.append(Sequence[i])
    countprot += 1
    if len(proteinseq) == testcount:
        break
for i in range(2, len(Sequence), 3):
    secondstruc.append(Sequence[i])
    if len(secondstruc) == testcount:
        break
SEQUENCE.close()
randomised = list(zip(protname,proteinseq,secondstruc))
protname = [randomised[i][0] for i in range(0, len(randomised))]
proteinseq = [randomised[i][1] for i in range(0, len(randomised))]
secondstruc = [randomised[i][2] for i in range(0, len(randomised))]

################################################################################
### Defining function for 'normalising' substitution matrix values
################################################################################
def sigmoid(x):
    return (1 / (1 + math.exp(-x)))

################################################################################
### Classifier
################################################################################
clf = RFC(n_jobs=-2, class_weight='balanced', n_estimators=250)
print ("Generating PSSM-Frequency Matrix predictor model with Random Forest Classifier and window size of 11...")
print ("Parameter:\n",clf)

################################################################################
### Collate the psi-blast PSSM profiles for each sequence.
################################################################################
combined_SM = []
secondarystruc = []
count = 0
for i in range(0,len(protname)):
    count += 1
    protnamepath = '../Datasets/>'+str(randomised[i][0])+'.fasta.pssm'
    secondarystruc.append(randomised[i][2])
    with open(protnamepath, 'r+') as PSSM:
        pssm = PSSM.read().splitlines()
        del pssm[0:3]
        del pssm[-6:]
        substitutionmatrix = [] #2-22
        for everyline in pssm:
            pssm_split = everyline.split()
            tmp_sm = pssm_split[22:42]
            tmp_sm2 = []
            for SM in tmp_sm:
                tmp_sm2.append(sigmoid(int(SM)))
            substitutionmatrix.append(tmp_sm2)
        combined_SM.append(substitutionmatrix)
################################################################################

classnames = ['(C) Coil', '(H) Helix', '(E) Sheet']
pad = [list(np.zeros(20))]

ws = 11
n = int((ws-1)/2)

SM_Windows = []
for protseq in combined_SM:
    countless = 0
    countmore = 0
    countrest = 0
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

################################################################################
### Preparing labels for testing
################################################################################
ss_map = {'C':1, 'H':2, 'S':3}
SM_label = []
for ss in secondarystruc:
    mappedfeat = [ss_map[attribute] for attribute in ss]
    SM_label.append(mappedfeat)
SM_label = [j for i in SM_label for j in i]

if len(SM_Windows) != len(SM_label):
    print ("Length of windows and label not equal. Quitting...")
    import sys
    sys.exit()

################################################################################
### Creating model
################################################################################
model = clf.fit(SM_Windows, SM_label)
joblib.dump(model, 'SM.pkl')
endtime = time.time() - start
print ("\nModel generated in %0.2f seconds.\n" %(endtime))
