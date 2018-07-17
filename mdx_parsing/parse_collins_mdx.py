from mdict_query import IndexBuilder
from bs4 import BeautifulSoup
import re
import csv
from collections import OrderedDict
import pymysql
builder=IndexBuilder('collins.mdx')

def getSentList(word):
    dict_str=builder.mdx_lookup(word)
    bs=BeautifulSoup(dict_str[0])
    l=bs.find_all('p',class_="C1_sentence_en")
    u=""
    for p in l:
        eng=p.text
        chn=p.find_next_sibling().text
        if chn.endswith("。"):
            if eng.startswith("..."):
                eng=eng[3:]
            if eng.endswith("..."):
                eng=eng[:-2]
            u+=eng+"\n"+chn+"\r\n"
    return u

conn = pymysql.connect(host='xxx', port=3306, user='root',passwd='xxx', db='ireading')

cur = conn.cursor()
keys=list(OrderedDict.fromkeys(builder.get_mdx_keys()))
"""
for key in keys:
    write (key,"".join(getSentList(key)))
"""

for key in keys:
    if key<'offscreen':
        continue
    try:
        sql = ('UPDATE word_mini '
            'SET collins_detail=\"{detail}\" '
            'WHERE word=\"{key}\"').format(detail=getSentList(key), key=key)
        cur.execute(sql)
        conn.commit()
        print (key)
    except:
        pass
