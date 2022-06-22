import re
import random as rd
f=open("Files/longText.txt","r",encoding="utf8")
text=f.read()
f.close()
result=""
need_len=4
first_index=rd.randint(0,len(text)-need_len-1)
string = text[first_index:first_index+need_len]
result+=string
print(string)
for i in range(100000):
    indexs=[m.start() for m in re.finditer(re.escape(string),text)]
    if len(indexs)==0:
        break
    index=rd.choice(indexs)
    string=text[index+1:index+1+need_len]
    if len(string)==1:
        string=string+" "
    if len(string)==string.count(string[0]):
        first_index = rd.randint(0, len(text) - need_len - 1)
        string = text[first_index:first_index + need_len]
    result+=string[-1]
    print(string)
print(result)
