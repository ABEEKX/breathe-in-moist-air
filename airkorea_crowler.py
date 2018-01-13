import urllib.request
from bs4 import BeautifulSoup
import time
import pymysql

url="http://www.airkorea.or.kr/index"
conn=pymysql.connect(host='52.78.192.119',port=3306,user='root',password='Cap2bowoo!',db='abeekx',charset='utf8')
cursor=conn.cursor()

while True:
    time.sleep(1)
    req=urllib.request.Request(url)
    data=urllib.request.urlopen(req).read()
    bs=BeautifulSoup(data,'html.parser')
    temp_pm10=bs.find(class_="f3 g2").text
    pm10=""
    for temp in temp_pm10:
        if(temp>='0' and temp<='9'):
            pm10+=temp
    print(pm10)
    sql='INSERT INTO airkorea (out_pm10) VALUES (%s)'
    cursor.execute(sql,(pm10))
    conn.commit()

conn.close()

