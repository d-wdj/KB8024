opentest = open('dssp_3state.3line.txt', 'r+')
opentest = opentest.read().splitlines()
protname = []
proteinseq = []
secondstruc = []
for i in range(0, len(opentest), 3):
    protname.append(opentest[i].lstrip('>'))
for i in range(1, len(opentest), 3):
    proteinseq.append(opentest[i])
for i in range(2, len(opentest), 3):
    secondstruc.append(opentest[i])
map = {'A':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7,
    'I':8, 'K':9, 'L':10, 'M':11, 'N':12, 'P':13, 'Q':14,
    'R':15, 'S':16, 'T':17, 'V':18, 'W':19, 'Y':20}
proteinseq2 = ''.join(proteinseq)
proteinseq2 = [map[char] for char in proteinseq2]
map = {'C':1, 'S':2, 'H':3}
secondstruc2 = ''.join(secondstruc)
secondstruc2 = [map[char] for char in secondstruc2]


protSStruc = list(zip(secondstruc2, proteinseq2))
print (protSStruc[:20])
#115271 lines_split into 5
b = open('MASTER.txt', 'w+')
b.write("# 1:A 2:C 3:D 4:E 5:F 6:G 7:H 8:I 9:K 10:L 11:M 12:N 13:P 14:Q 15:R 16:S 17:T 18:V 19:W 20:Y\n")
for element in protSStruc:
    a = str(element)
    a = a.lstrip('(').rstrip(')').replace(',','')
    b.write(a+':1' + '\n')

test1 = open('test1.txt', 'w+')
test1.write("# 1:A 2:C 3:D 4:E 5:F 6:G 7:H 8:I 9:K 10:L 11:M 12:N 13:P 14:Q 15:R 16:S 17:T 18:V 19:W 20:Y\n")
for element in protSStruc[0:23054]:
    a = str(element)
    a = a.lstrip('(').rstrip(')').replace(',','')
    test1.write(a+':1' + '\n')

test2 = open('test2.txt', 'w+')
test2.write("# 1:A 2:C 3:D 4:E 5:F 6:G 7:H 8:I 9:K 10:L 11:M 12:N 13:P 14:Q 15:R 16:S 17:T 18:V 19:W 20:Y\n")
for element in protSStruc[23054:(2*23054)]:
    a = str(element)
    a = a.lstrip('(').rstrip(')').replace(',','')
    test2.write(a+':1' + '\n')

test3 = open('test3.txt', 'w+')
test3.write("# 1:A 2:C 3:D 4:E 5:F 6:G 7:H 8:I 9:K 10:L 11:M 12:N 13:P 14:Q 15:R 16:S 17:T 18:V 19:W 20:Y\n")
for element in protSStruc[(2*23054):(3*23054)]:
    a = str(element)
    a = a.lstrip('(').rstrip(')').replace(',','')
    test3.write(a+':1' + '\n')

test4 = open('test4.txt', 'w+')
test4.write("# 1:A 2:C 3:D 4:E 5:F 6:G 7:H 8:I 9:K 10:L 11:M 12:N 13:P 14:Q 15:R 16:S 17:T 18:V 19:W 20:Y\n")
for element in protSStruc[(3*23054):(4*23054)]:
    a = str(element)
    a = a.lstrip('(').rstrip(')').replace(',','')
    test4.write(a+':1' + '\n')

test5 = open('test5.txt', 'w+')
test5.write("# 1:A 2:C 3:D 4:E 5:F 6:G 7:H 8:I 9:K 10:L 11:M 12:N 13:P 14:Q 15:R 16:S 17:T 18:V 19:W 20:Y\n")
for element in protSStruc[(4*23054):(5*23054)+1]:
    a = str(element)
    a = a.lstrip('(').rstrip(')').replace(',','')
    test5.write(a+':1' + '\n')

train1 = open('train1.txt', 'w+')
train1.write("# 1:A 2:C 3:D 4:E 5:F 6:G 7:H 8:I 9:K 10:L 11:M 12:N 13:P 14:Q 15:R 16:S 17:T 18:V 19:W 20:Y\n")
for element in protSStruc[(2*23054):(5*23054)+1]:
    a = str(element)
    a = a.lstrip('(').rstrip(')').replace(',','')
    train1.write(a+':1' + '\n')

train2 = open('train2.txt', 'w+')
train2.write("# 1:A 2:C 3:D 4:E 5:F 6:G 7:H 8:I 9:K 10:L 11:M 12:N 13:P 14:Q 15:R 16:S 17:T 18:V 19:W 20:Y\n")
for element in protSStruc[0:23054]:
    a = str(element)
    a = a.lstrip('(').rstrip(')').replace(',','')
    train2.write(a+':1' + '\n')
for element in protSStruc[(2*23054):(5*23054)+1]:
    a = str(element)
    a = a.lstrip('(').rstrip(')').replace(',','')
    train2.write(a+':1' + '\n')

train3 = open('train3.txt', 'w+')
train3.write("# 1:A 2:C 3:D 4:E 5:F 6:G 7:H 8:I 9:K 10:L 11:M 12:N 13:P 14:Q 15:R 16:S 17:T 18:V 19:W 20:Y\n")
for element in protSStruc[0:(2*23054)]:
    a = str(element)
    a = a.lstrip('(').rstrip(')').replace(',','')
    train3.write(a+':1' + '\n')
for element in protSStruc[(3*23054):(5*23054)+1]:
    a = str(element)
    a = a.lstrip('(').rstrip(')').replace(',','')
    train3.write(a+':1' + '\n')

train4 = open('train4.txt', 'w+')
train4.write("# 1:A 2:C 3:D 4:E 5:F 6:G 7:H 8:I 9:K 10:L 11:M 12:N 13:P 14:Q 15:R 16:S 17:T 18:V 19:W 20:Y\n")
for element in protSStruc[0:(3*23054)]:
    a = str(element)
    a = a.lstrip('(').rstrip(')').replace(',','')
    train4.write(a+':1' + '\n')
for element in protSStruc[(4*23054):(5*23054)+1]:
    a = str(element)
    a = a.lstrip('(').rstrip(')').replace(',','')
    train4.write(a+':1' + '\n')

train5 = open('train5.txt', 'w+')
train5.write("# 1:A 2:C 3:D 4:E 5:F 6:G 7:H 8:I 9:K 10:L 11:M 12:N 13:P 14:Q 15:R 16:S 17:T 18:V 19:W 20:Y\n")
for element in protSStruc[0:(4*23054)]:
    a = str(element)
    a = a.lstrip('(').rstrip(')').replace(',','')
    train5.write(a+':1' + '\n')

###


# result = []
# print (type(proteinseq2))
# print (type(secondstruc2))
# for element in proteinseq2:
#     for elementss in secondstruc2:
#         result.append(str(elementss) + ' ' + str(element))
# print (result)
# for i in range(0, len(opentest)):
#     if (opentest.readline(i)).startswith('>'):
#         protname.append(opentest.readline(i))
    # for everyline in opentest:
    #     if everyline.startswith('>'):
    #         protname.append(everyline.lstrip('>').rstrip('\n'))
    #     else:
    #         proteinseq.append(everyline)
    #         secondstruc.append(everyline)
# print (protname)
# for everychar in proteinseq:
#     print (everychar)
# ProteinSStruc = dict(zip(proteinseq, secondstruc))
# vec = DictVectorizer()
# vec.fit_transform(ProteinSStruc).toarray()
# print (vec.get_feature_names())
#print (genename[:20], proteinseq[:20], secondstruc[:20])
# dProtein = dict(zip(genename, proteinseq))
# dSecondst = dict(zip(genename, secondstruc))
# print (dProtein, dSecondst)
