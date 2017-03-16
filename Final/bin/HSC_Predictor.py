#!/usr/bin/python
import time
import os.path
import sys
from sklearn import preprocessing
from sklearn.externals import joblib

print ("---SINGLE SEQUENCE-BASED PREDICTOR---")
print ("Loading model...")
clf = joblib.load('HSC.pkl')
print ("Model acquired. Ready to predict.")

user_input = open(sys.argv[1], 'r+')
work_input = user_input.read().splitlines()

newpath = '../Results/'
if not os.path.exists(newpath):
    os.makedirs(newpath)

AA_map = {'0':0, 'A':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7,
        'I':8, 'K':9, 'L':10, 'M':11, 'N':12, 'P':13, 'Q':14,
        'R':15, 'S':16, 'T':17, 'V':18, 'W':19, 'Y':20}
ss_map = {'C':1, 'H':2, 'S':3}
print ("Preparing input protein(s)...")
countprot = 0
i_protname = [work_input[i] for i in range(0, len(work_input),2)]
i_proteinseq = [work_input[i] for i in range(1, len(work_input),2)]
for i in i_proteinseq:
    countprot += 1

user_input.close()
print ("Number of sequences: ",countprot)
inv_ss_map = {1:'C', 2:'H', 3:'E'}
pred = []
ws = 11
n = int(ws/2)
enc = preprocessing.OneHotEncoder(n_values=21)
countprot = 0
total = len(i_proteinseq)

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

pad = [0]
for eachprotein in i_proteinseq:
    countprot += 1
    eachprot =  []
    protseq = [AA_map[i] for i in eachprotein]
    protlen = len(protseq)
    for i in range(0, len(protseq)):
        if i < n:
            eachprot.append((pad*(n-i)) + protseq[0:ws-(n-i)])
        elif i >= (len(protseq)-n):
            addprot = protseq[(i-n):ws-(n-i)+1]
            if len(addprot) != ws:
                addprot.extend(pad*(ws-len(addprot)))
            eachprot.append(addprot)
        else:
            eachprot.append(protseq[(i-n):(i+n+1)])
    print ("Predicting sequence %d/%d..." %(countprot, total))
    ep_T = enc.fit_transform(eachprot).toarray()
    prediction = list(clf.predict(ep_T))
    prediction = [inv_ss_map[i] for i in prediction]
    prediction = ''.join(prediction)
    if (sys.argv[3] == 'y') or (sys.argv[3] == 'Y'):
        print (i_protname[countprot-1])
        print (prediction)
    pred.append(prediction)

print ("Writing prediction output into %s..." %(newpath+'HSC_'+sys.argv[2]))
runtime = time.strftime("%Y-%m-%d %H:%M %Z")
with open((newpath+'HSC_'+sys.argv[2]), 'w+') as op:
    op.write("HSCPred Single-sequence-based prediction "+runtime+'\n')
    for i in range(0, len(i_protname)):
        op.write(str(i_protname[i])+'\n')
        op.write(str(i_proteinseq[i])+'\n')
        op.write(str(pred[i])+'\n')
    op.write("Generated using HSCPred -- (C)2017 - Dimitri Wirjowerdojo ")

print ("\nHSC Prediction finished. Have a good day!\n")
