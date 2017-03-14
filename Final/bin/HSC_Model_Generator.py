import time
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn import preprocessing
from sklearn.externals import joblib

## SECTION 1: OPENING FILE AND APPENDING INTO LISTS
################################################################################
### Opens the file and appends each feature of the file into
### the appropriate lists.
################################################################################
# SEQUENCE = input("Please specify the directory and the name of the dataset for the model:\n")
# SEQUENCE = open(SEQUENCE, 'r+')
SEQUENCE = open('../Datasets/dssp_3state.3line.txt', 'r+')
Sequence = SEQUENCE.read().splitlines()

clf = RFC(n_jobs=-2, class_weight='balanced', n_estimators=300)
print ("Generating single-sequence predictor model with Random Forest Classifier  and window size of 11...")
print ("Parameter:\n",clf)
start = time.time()
countprot = int(len(Sequence)/3)
protname = [Sequence[i] for i in range(0, len(Sequence),3)]
proteinseq = [Sequence[i] for i in range(1, len(Sequence),3)]
secondstruc = [Sequence[i] for i in range(2, len(Sequence),3)]
SEQUENCE.close()


ws = 11
n = int(ws/2)

# SECTION 2: CREATE SLIDING WINDOWS
################################################################################
### With window size = input, break down the protein sequence with
### overlaps/sliding window.
################################################################################
AA_map = {'0':0, 'A':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7,
        'I':8, 'K':9, 'L':10, 'M':11, 'N':12, 'P':13, 'Q':14,
        'R':15, 'S':16, 'T':17, 'V':18, 'W':19, 'Y':20}
pad = [0]
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

# SECTION 3: MAP THE STRUCTURE LABELS
################################################################################
### Ibid
################################################################################
structrip = []
ss_map = {'C':1, 'H':2, 'S':3}
for secondsec in secondstruc:
    mappedfeat = [ss_map[attribute] for attribute in secondsec]
    structrip.append(mappedfeat)
structrip = [subelement for element in structrip for subelement in element]

# SECTION 4: DATA TRANSFORMATION AND MODEL GENERATION
################################################################################
### List of windows is encoded
################################################################################
enc = preprocessing.OneHotEncoder()#n_values=20)
mappedprotein_encoded = enc.fit_transform(protriplets).toarray()
model = clf.fit(mappedprotein_encoded, structrip)
joblib.dump(model, 'HSC.pkl')
endtime = time.time() - start
print ("\nModel generated in %0.2f seconds.\n" %(endtime))

################################################################################
################################################################################
################################################################################
