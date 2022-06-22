from random import choice as ch
from random import random as rd
f=open("Files/words","r",encoding="utf-8")
lines=f.readlines()
f.close()

english=[]
ukrain=[]
b=True
for line in lines:
    line=line[:-1]
    if line=="":
        b=not b
        continue
    line=line[line.find(" ")+2:]
    if b:
        english.append(line)
    else:
        ukrain.append(line)


b=input('eng->ukr? ')!=""

d={}

indexs = [i for i in range(len(english))]
indexs.sort(key=lambda x: rd())

for i in range(len(english)):
    if not b:
        d[english[indexs[i]]]=ukrain[indexs[i]]
    else:
        d[ukrain[indexs[i]]] = english[indexs[i]]
first=list(d.keys())
last=list(d.values())
[print(" "*50+f"{i+1}) "+first[i]) for i in range(len(english))]
input()
print("\n"*10)
[print(" "*40+f"{i+1}) "+first[i]+" "+"-"*(50-len(first[i])-len(f"{i+1}"))+" "+last[i]) for i in range(len(english))]
print("\n"*10)