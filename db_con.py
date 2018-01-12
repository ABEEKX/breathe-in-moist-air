import pymysql

con=pymysql.connect(host='52.78.192.119',port=3306,user='root',password='Cap2bowoo!',db='abeekx',charset='utf8')
cursor1=con.cursor()
cursor1.execute("SELECT * FROM predict")

'''flag=False
for row in cursor1:
    cur_ppm = float(row[0])
    if(flag):
        if(cur_ppm-pre_ppm>3000.0):
            print(pre_ppm)
        else:
            print(cur_ppm)
    else:
        print(cur_ppm)
    pre_ppm = cur_ppm
    flag=True
'''

cursor1.close()
con.close()