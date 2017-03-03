from sklearn import preprocessing
import numpy as np
from sklearn import svm
from sklearn.model_selection import cross_val_score
from sklearn.utils import shuffle
import os.path


# SECTION 1: OPENING FILE AND APPENDING INTO LISTS
################################################################################
### Opens the file and appends each feature of the file into
### the appropriate lists.
################################################################################
promptfile = input("Please specify directory, name and format of the file: ")
SEQUENCE = open(promptfile, 'r+')
# SEQUENCE = open('../Datasets/sample_60.txt', 'r+')
Sequence = SEQUENCE.read().splitlines()
print ("Opening the files and appending data features into their lists...")
countprot = int(len(Sequence)/3)
protname = [Sequence[i] for i in range(0, len(Sequence),3)]
proteinseq = [Sequence[i] for i in range(1, len(Sequence),3)]
secondstruc = [Sequence[i] for i in range(2, len(Sequence),3)]

# for i in range(0, len(Sequence), 3):
#     protname.append(Sequence[i].lstrip('>'))
# for i in range(1, len(Sequence), 3):
#     proteinseq.append(Sequence[i])
#     countprot += 1
# for i in range(2, len(Sequence), 3):
#     secondstruc.append(Sequence[i])
SEQUENCE.close()
print ("Number of sequences: ",countprot)

# SECTION 2: PROMPT FOR WINDOW SIZE
################################################################################
### Condition to check whether the input integer is odd and >= than 3.
################################################################################
while True:
    ws = input("Please specify an odd integer >= 3 for window size: ")
    if int(ws) != 1 and (int(ws)%2 == 1):
        ws = int(ws)
        n = int(ws/2)
        break
# n = int(ws/2)

# SECTION 3: MAKE DIRECTORY FOR SPECIFIED WINDOW SIZE
################################################################################
### Make directory for each window size
################################################################################
# newpath = '../Datasets/Window Size/'+str(ws)+'/'
# if not os.path.exists(newpath):
#     os.makedirs(newpath)
#     os.makedirs(newpath+'Train Set')
#     os.makedirs(newpath+'Test Set')

# SECTION 4: EXTRACT PROTEIN NAME AND PROTEIN SEQUENCE INTO A FASTA FILE
################################################################################
### Writing the protname and proteinseq into another file.fasta for psi-blast
################################################################################
# fastaname = 'fasta'+str(countprot)+'.fasta'
# printpath = newpath + fastaname
# with open(printpath, 'w+') as write:
#     a = "Number of proteins: "+str(countprot)
#     write.write(a)
#     for i in range(0,len(protname)):
#         write.write(('>'+str(protname[i])+'\n'))
#         write.write((str(proteinseq[i])+'\n'))

# SECTION 5: CREATE SLIDING WINDOWS
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

## SECTION 6: MAPPING
# SECTION 6.1: MAP PROTEINS TO NUMBERS
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
#mappedprotein = [subelement for element in mappedprotein for subelement in element]
print("Length mapped protein: ", (len(mappedprotein)))

# SECTION 6.2: MAP FEATURES TO NUMBERS
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
print("Length mapped features: ", (len(structrip)))

# SECTION 6.3: CHECKING IF NUMBERS OF FEATURES = THAT OF PROTEIN
###############################################################################
## Checking if number of windows is equal to the number of features.
###############################################################################
countstruc = 0
for i in structrip:
    countstruc += 1
counttrip = 0
for i in mappedprotein:
    counttrip += 1
if countstruc != counttrip:
    print ("Number of window is not equal to number of features.")
    print ("No. of windows:",counttrip, "No. of features:",countstruc)

## SECTION 7: PRINTING INTO FILE
# SECTION 7.1: PRINTING A MASTER FILE
################################################################################
### Printing everything into a file; window and feature separated by comma.
################################################################################
# name = '../Datasets/Window Size/'+str(ws)+'/MASTER'+(str(ws))+'.txt'
# with open(name, 'w+') as output:
#     for i in range(0, len(mappedprotein)):
#         output.write(str(mappedprotein[i])+'+'+str(structrip[i])+'\n')

# SECTION 7.2: PRINTING TEST AND TRAIN SETS
################################################################################
### Generating N number test and train set files, with N from user input.
################################################################################
# while True:
#     fileno = input("Please specify the number of files it should be split into: ")
#     if type(fileno) != 'int':
#         fileno = int(fileno)
#         break
# len_total = len(mappedprotein)
# for testset_number in range(1, (fileno+1)):
#     testset_name = 'testset'+str(testset_number)+'.txt'
#     pr_begin = int(((testset_number-1)/fileno)*(len_total))
#     pr_end = int((testset_number/fileno)*(len_total))
#     # print (pr_begin, pr_end)
#     printpath = newpath+'Test Set/'+ testset_name
#     with open(printpath, 'w+') as testoutput:
#         for i in range(pr_begin, pr_end-1):
#                 for emp in mappedprotein[i]:
#                     testoutput.write(str(emp)+' ')
#                 testoutput.write('\n'+str(structrip[i])+'\n')
# print ("File has been split into", fileno, "testsets.")
#
# LON = list(range(1, (fileno+1)))
# for i in LON:
#     listofnumbers = list(range(1, (fileno+1)))
#     del (listofnumbers[i-1])
#     trainset_name = 'trainset'+str(i)+'.txt'
#     printpath = newpath+'Train Set/'+ trainset_name
#     with open(printpath, 'w+') as testoutput:
#         for notnumber in listofnumbers:
#             pr_begin = int(((notnumber-1)/fileno)*(len_total))
#             pr_end = int((notnumber/fileno)*(len_total))
#             for i in range(pr_begin, pr_end):
#                 for emp in mappedprotein[i]:
#                     testoutput.write(str(emp)+' ')
#                 testoutput.write('\n'+str(structrip[i])+'\n')
# print ("File has been split into", fileno, "trainsets.")
print ("Feature extraction finished.")
################################################################################

# SECTION 8: PRINTING SKLEARN INPUTS
################################################################################
###
################################################################################
enc = preprocessing.OneHotEncoder()
mappedprotein_encoded = enc.fit_transform(mappedprotein).toarray()
print ("Some examples for SKLearn inputs:")
for i in range(0, 120, 40):
    a = mappedprotein_encoded[i]
    b = structrip[i]
    print (a,b)

################################################################################
################################################################################
print ("Job finished. Have a good day!\n")
