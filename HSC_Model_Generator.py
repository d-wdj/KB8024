import os.path
import time
import numpy as np
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn import preprocessing
from sklearn.externals import joblib
from sklearn import preprocessing

print ("(C)2017 Dimitri Wirjowerdojo - KI/KTH/SU-Stockholm, Sweden.")
print ("This is a programme which you can use to predict the secondary structure of an input protein.")
print ("The model is based on 399 proteins with DSSP assignments.\n")

## SECTION 1: OPENING FILE AND APPENDING INTO LISTS
################################################################################
### Opens the file and appends each feature of the file into
### the appropriate lists.
################################################################################
# SEQUENCE = input("Please specify the directory and the name of the dataset for the model:\n")
# SEQUENCE = open(SEQUENCE, 'r+')
SEQUENCE = open('../../Datasets/dssp_3state.3line.txt', 'r+')
Sequence = SEQUENCE.read().splitlines()

clf = RFC()
print ("Generating model with Random Forest Classifier with a window size of 9...")
print ("Parameter:\n",clf)
start = time.time()
countprot = int(len(Sequence)/3)
protname = [Sequence[i] for i in range(0, len(Sequence),3)]
proteinseq = [Sequence[i] for i in range(1, len(Sequence),3)]
secondstruc = [Sequence[i] for i in range(2, len(Sequence),3)]
SEQUENCE.close()

## SECTION 2: PROMPT FOR WINDOW SIZE
################################################################################
### Condition to check whether the input integer is odd and >= than 3.
################################################################################
### still waiting for the most optimal parameter for window size and SVM
### most probably will use WS of 11 for SS prediction (cf. paper)
# while True:
#     ws = input("Please specify an odd integer >= 3 for window size: ")
#     if int(ws) != 1 and (int(ws)%2 == 1):
#         ws = int(ws)
#         n = int(ws/2)
#         break
ws = 9
n = int(ws/2)

# SECTION 3: CREATE SLIDING WINDOWS
################################################################################
### With window size = input, break down the protein sequence with
### overlaps/sliding window.
################################################################################
AA_map = {'0':0, 'A':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7,
        'I':8, 'K':9, 'L':10, 'M':11, 'N':12, 'P':13, 'Q':14,
        'R':15, 'S':16, 'T':17, 'V':18, 'W':19, 'Y':20}
pad = [0]#*20
protriplets = []
eachprot = []
for protseq in proteinseq:
    protseq = [AA_map[i] for i in protseq]
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
    protriplets.append(eachprot)
    eachprot = []
protriplets = [j for i in protriplets for j in i]
#     eachprot = []
#     for i in range(0, protlen):
#         if i < n:
#             # print (protseq[0:ws-(n-i)+1])
#             eachprot.append([(pad*(n-i))+protseq[0:ws-(n-i)]])
#         elif i > protlen-n:
#             eachprot.append([protseq[0:ws-(n-i)+1]+(pad*(n))])
#         else:
#             eachprot.append([protseq[(i-n):(i+1+n)]])
#     eachprot = [j for i in eachprot for j in i]
#     protriplets.append(eachprot)
#
# print (protriplets[0])
# import sys
# sys.exit()
# for protseq in proteinseq:
#     protseq = ((n)*'0')+protseq+((n)*'0')
#     for i in range(0, len(protseq)):
#         if i+(ws) > len(protseq):
#             break
#         temp = protseq[i:i+(ws)]
#         protriplets.append(temp)

## SECTION 4: MAPPING
# SECTION 4.1: MAP PROTEINS TO NUMBERS
################################################################################
### Mapping protein into their assigned numbers.
################################################################################
# mappedprotein = []
# AA_map = {'0':0, 'A':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7,
#         'I':8, 'K':9, 'L':10, 'M':11, 'N':12, 'P':13, 'Q':14,
#         'R':15, 'S':16, 'T':17, 'V':18, 'W':19, 'Y':20}
# for element in protriplets:
#     tmp = []
#     for character in element:
#         tmp2 = AA_map[character]
#         tmp.append(tmp2)
#     mappedprotein.append(tmp)
#mappedprotein = [subelement for element in mappedprotein for subelement in element]

# SECTION 4.2: MAP FEATURES TO NUMBERS
################################################################################
### Similarly, trying to create a list containing the features.
################################################################################
structrip = []
ss_map = {'C':1, 'H':2, 'S':3}
for secondsec in secondstruc:
    mappedfeat = [ss_map[attribute] for attribute in secondsec]
    structrip.append(mappedfeat)
structrip = [subelement for element in structrip for subelement in element]

# SECTION 5: DATA TRANSFORMATION AND MODEL GENERATION
################################################################################
### List of windows is encoded
################################################################################
enc = preprocessing.OneHotEncoder()#n_values=20)
mappedprotein_encoded = enc.fit_transform(protriplets).toarray()
model = clf.fit(mappedprotein_encoded, structrip)
joblib.dump(model, 'DSSP_3Class_Model_HSC.pkl')
endtime = time.time() - start
print ("Model generated in %f seconds.\n\n" %(endtime))

################################################################################
################################################################################
################################################################################
