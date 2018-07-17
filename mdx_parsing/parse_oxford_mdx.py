from mdict_query import IndexBuilder
from bs4 import BeautifulSoup
import re
from collections import OrderedDict

builder=IndexBuilder('oxford.mdx')

def getSentList(word):
    dict_str=builder.mdx_lookup(word)
    bs=BeautifulSoup(dict_str[0])
    l=bs.find_all('span',class_="x")
    u=[]
    for span in l:
        if "." not in span.text and "?" not in span.text and "!" not in span.text:
            continue
        contents= span.contents
        if len(contents)>3:
            continue
        chn=span.find_next_sibling().text

        if len(contents)==1:
            eng=contents[0]
        elif len(contents)==3:
            temp=['','','']
            for i in range(3):
                if hasattr(contents[i],'text'):
                    if contents[i].findChild():
                        continue
                    temp[i]=contents[i].text
                else:
                    temp[i]=re.sub('\r\n(\s)+','',contents[i])
            eng=temp[0]+' '+temp[1]+' '+temp[2]


        elif len(contents)==2:
            print (222)
            print (span)
            temp=['','']
            for i in range(2):
                if hasattr(contents[i],'text'):
                    if contents[i].findChild():
                        continue
                    temp[i]=contents[i].text
                else:
                    temp[i]=re.sub('\r\n(\s)+','',contents[i])
            eng=temp[0]+' '+temp[1]
        if not eng.endswith("\n"):
            eng+="\n"
        u.append(eng+chn+"\r\n")
    return u


keys=list(OrderedDict.fromkeys(builder.get_mdx_keys()))
"""
for key in keys:
    write (key,"".join(getSentList(key)))
"""

for key in keys[1100:1120]:
    print (key)
    print ("".join(getSentList(key)))
