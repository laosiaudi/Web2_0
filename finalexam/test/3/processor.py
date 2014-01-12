#coding=utf-8

rfile = open("input.txt",'r')
lines = rfile.readlines()
count = {}
for word in lines:
    word = word[:-2]
    if not count.has_key(word):
        count[word] = 1
    else:
        count[word] += 1

newlist = sorted(count.iteritems(),key=lambda item:item[1],reverse = True)
newdic = {}
for item in newlist:
    if not newdic.has_key(item[1]):
        templist = []
        templist.append(item[0])
        newdic[item[1]] = templist
    else:
        newdic[item[1]].append(item[0])
wfile = open("results.txt",'w')
index = 0
keys = newdic.keys()
keys.sort(reverse = True)
for iem in keys:
    index = 0
    wfile.write('count ' + str(iem) + ': [')
    templist = newdic[iem]
    templist = sorted(templist)
    for key in templist:
        if index == 0:
            wfile.write("'" + key + "'" )
        else:
            wfile.write(", '" + key + "'")
        index += 1

    wfile.write(']\n')
wfile.close()
rfile.close()

