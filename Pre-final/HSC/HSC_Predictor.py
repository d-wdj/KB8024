import os.path
from sklearn import preprocessing
from sklearn.externals import joblib


print ("(C)2017 Dimitri Wirjowerdojo - KI/KTH/SU-Stockholm, Sweden.")
print ("This is a programme which you can use to predict the secondary structure of an input protein.")
print ("The model is based on 399 proteins with DSSP 3-class assignments.\n\n")

print ("Loading model...")
clf = joblib.load('DSSP_3Class_Model_HSC.pkl')
# print (clf)
print ("Model acquired. Ready to predict.")
print ("Input sequence must be in a fasta-format, without empty line separation between each sequence.")

user_input = input("Please specify the directory and the name of your fasta-format file:\n")
user_input = open(user_input, 'r+')
# user_input = open("../../Datasets/test_predict.txt", 'r+')
work_input = user_input.read().splitlines()

print ("Creating a directory for results...")
newpath = 'Results/'
if not os.path.exists(newpath):
    os.makedirs(newpath)

AA_map = {'0':0, 'A':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7,
        'I':8, 'K':9, 'L':10, 'M':11, 'N':12, 'P':13, 'Q':14,
        'R':15, 'S':16, 'T':17, 'V':18, 'W':19, 'Y':20}
ss_map = {'C':1, 'H':2, 'S':3}
print ("Preparing input protein(s)...")
i_protname = [work_input[i] for i in range(0, len(work_input),2)]
i_proteinseq = [work_input[i] for i in range(1, len(work_input),2)]

output_name = input("Please specify name and format for output:\n")
# output_name = 'predict_output.txt'

inv_ss_map = {1:'C', 2:'H', 3:'S'}
pred = []
ws = 9
n = 4
enc = preprocessing.OneHotEncoder()#n_values=21)
countprot = 0
total = len(i_proteinseq)

### Check for non-standard amino acids #########################################
for eachsequence in range(0, len(i_proteinseq)):
    for AA in range(0, len(i_proteinseq[eachsequence])):
        eachresidue = i_proteinseq[eachsequence][AA]
        if (eachresidue == 'B') or (eachresidue == 'J') or (eachresidue == 'U') or (eachresidue == 'X'):
            print ("Non-standard amino acid '%s' detected in sequence %s position %d. Quitting..."
                    %(eachresidue, i_protname[eachsequence], AA))
            import sys
            sys.exit()
################################################################################
while True:
    check = input("Would you like to see the prediction [y/n]? ")
    if (check == 'Y') or (check == 'y') or (check == 'N') or (check == 'n'):
        break

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
    ep_T = enc.fit_transform(eachprot).toarray() ## Encoding for prediction
    prediction = list(clf.predict(ep_T))
    prediction = [inv_ss_map[i] for i in prediction]
    prediction = ''.join(prediction)
    if (check == 'y') or (check == 'Y'):
        print (i_protname[countprot-1])
        print (prediction)
    pred.append(prediction)

print ("Writing prediction output into %s..." %(newpath+output_name))
with open((newpath+output_name), 'w+') as op:
    for i in range(0, len(i_protname)):
        op.write(str(i_protname[i])+'\n')
        op.write(str(i_proteinseq[i])+'\n')
        op.write(str(pred[i])+'\n')

print ("\n\nPrediction finished. Have a good day!")
