# -*- coding=utf-8 -*-
import csv  # 加载csv包便于读取csv文件
import json
from time import sleep

from pip._vendor import requests
from pip._vendor.requests.adapters import HTTPAdapter
from pip._vendor.requests.packages.urllib3 import Retry

session = requests.Session()
retry = Retry(connect=10000, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

import pymysql

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='23333', db='ireading')

cur = conn.cursor()
cur.execute("SELECT Max(id) from word_mini where (uk_pron is not null and us_pron is not null)")
for item in cur:
    index = item[0]
cur.execute("SELECT word from word_mini where id>" + str(index))
l = []
c=0
count = index
for item in cur:
    l.append(item[0])
print('finish')
for word in l:
    print(word, count,c)
    count += 1
    params = {'w': word.lower(), 'key': '341DEFE6E5CA504E62A567082590D0BD', 'type': 'json'}
    xml_bytes = session.get(
        'http://dict-co.iciba.com/api/dictionary.php', params=params).text
    d = json.loads(xml_bytes)['symbols'][0]
    if 'ph_am' in d:
        if d['ph_am']:
            sql = ('UPDATE word_mini '
                   'SET us_pron=\"{pron}\" '
                   'WHERE word=\"{key}\"').format(pron=d['ph_am'][:45], key=word)
            cur.execute(sql)
            conn.commit()

            c+=1
    if 'ph_en' in d:
        if d['ph_en']:
            sql = ('UPDATE word_mini '
                   'SET uk_pron=\"{pron}\" '
                   'WHERE word=\"{key}\"').format(pron=d['ph_en'][:45], key=word)
            conn.commit()
            cur.execute(sql)
            c+=1
    if c>=50:
        conn.commit()
        c=0
        print('commit')