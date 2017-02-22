import numpy as np
from sklearn import svm
from sklearn import preprocessing

################################################################################
### Opens the file and appends each feature of the file into
### the appropriate lists.
################################################################################
promptfile = input("Please specify filename and format: ")
SEQUENCE = open(promptfile, 'r+')
# SEQUENCE = open('dssp_3state.3line.txt', 'r+')
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

################################################################################
### Condition to check whether the input integer is odd and >= than 3.
################################################################################
while True:
    ws = input("Please specify an odd integer >= 3 for window size: ")
    if int(ws) != 1:
        if (type(ws) == 'int') or (int(ws)%2 == 1):
            ws = int(ws)
            n = int(ws/2)
            break

################################################################################
### With window size = input, break down the protein sequence with
### overlaps/sliding window.
################################################################################
print ("Breaking down sequences into windows and have them mapped...")
protriplets = []
for protseq in proteinseq:
    protseq = ((n)*'0')+protseq+((n)*'0')
    for i in range(0, len(protseq)):
        if i+(ws) > len(protseq):
            break
        temp = protseq[i:i+(ws)]
        protriplets.append(temp)

################################################################################
### Mapping protein into their assigned numbers.
################################################################################
mappedprotein = []
map = {'0':0, 'A':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7,
        'I':8, 'K':9, 'L':10, 'M':11, 'N':12, 'P':13, 'Q':14,
        'R':15, 'S':16, 'T':17, 'V':18, 'W':19, 'Y':20}
for element in protriplets:
    tmp = []
    for character in element:
        tmp2 = map[character]
        tmp.append(tmp2)
    mappedprotein.append(tmp)

################################################################################
### Similarly, trying to create a list containing the features.
################################################################################
print ("Breaking down features and have them mapped...")
structrip = []
map = {'C':1, 'H':2, 'S':3}
for secondsec in secondstruc:
    mappedfeat = [map[attribute] for attribute in secondsec]
    structrip.append(mappedfeat)
structrip = [subelement for element in structrip for subelement in element]

################################################################################
### Checking if number of windows is equal to the number of features.
################################################################################
countstruc = 0
for i in structrip:
    countstruc += 1
counttrip = 0
for i in mappedprotein:
    counttrip += 1
if countstruc != counttrip:
    print ("Number of window is not equal to number of features.")
    print ("No. of windows:",counttrip, "No. of features:",countstruc)

################################################################################
### Doing one hot encoding to map every single window to 'binary' format
################################################################################
print ("One hot encoding...")
enc = preprocessing.OneHotEncoder()
A = enc.fit_transform(mappedprotein).toarray()
#B = enc.transform(mappedprotein).toarray()
# print (A[0])

################################################################################
### Running the SVM algorithm
################################################################################
print ("SVM...")
lin_clf = svm.LinearSVC()
print (lin_clf.fit(A, structrip))
# clf = svm.SVC()  #decision_function_shape='ovr')
# print (clf.fit(B, structrip))
