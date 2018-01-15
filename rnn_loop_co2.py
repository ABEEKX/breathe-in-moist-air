import tensorflow as tf
import numpy as np
import pymysql
import datetime

seq_length = 7
data_dim = 1
hidden_dim = 10
output_dim = 1
#num_layer = 3


# connect db
con=pymysql.connect(host='52.78.192.119',port=3306,user='root',password='Cap2bowoo!',db='abeekx',charset='utf8')
cursor=con.cursor()

# if new data input then start main
cursor.execute("SELECT MAX(id) FROM sensors")  # check new data in
pre_max_id=int(cursor.fetchone()[0])

max_id = pre_max_id
while( max_id == pre_max_id ):
    con.commit()
    cursor.execute("SELECT MAX(id) FROM sensors")
    max_id=int(cursor.fetchone()[0])

# main
cursor.execute("SELECT ppm,time FROM sensors")
xy=[]
time=[]

# noisy data handling
flag=False
for row in cursor:
    cur_ppm = float(row[0])
    time.append([str(row[1])])  # get timestamp
    if(flag):
        if(cur_ppm-pre_ppm>3000.0):
            xy.append([pre_ppm])
            cur_ppm=pre_ppm
        else:
            xy.append([cur_ppm])
    else:
        xy.append([cur_ppm])
    pre_ppm = cur_ppm
    flag=True

last_time=time[-1]

xy1=xy  # pre Scalar data
numerator = xy - np.min(xy, 0)  # MinMaxScalar
denominator = np.max(xy, 0) - np.min(xy, 0)
xy = (xy - np.min(xy, 0))/ (denominator + 1e-7)
x = xy

dataX = []
dataY = []
for i in range(0, len(x) - seq_length):
    _x = x[i:i + seq_length]
    _y = x[i+seq_length]
    dataX.append(_x)
    dataY.append(_y)

# train/test split
train_size = int(0.95*len(dataX))
trainX, testX = np.array(dataX[0:train_size]), np.array(dataX[train_size:len(dataX)])
trainY, testY = np.array(dataY[0:train_size]), np.array(dataY[train_size:len(dataY)])
timeY = np.array(time[train_size:len(dataY)])

X = tf.placeholder(tf.float32, [None, seq_length, data_dim])
Y = tf.placeholder(tf.float32, [None,  data_dim])

# build a LSTM network
cell = tf.contrib.rnn.BasicLSTMCell(num_units=hidden_dim, state_is_tuple=True, activation=tf.tanh)
'''Multi Layer LSTM network
cells = []
for _ in range(num_layers):
  cell = tf.contrib.rnn.BasicLSTMCell(num_units=hidden_dim, state_is_tuple=True, activation=tf.tanh)
  cell = tf.contrib.rnn.DropoutWrapper(cell, output_keep_prob=0.8)
  cells.append(cell)
cell = tf.contrib.rnn.MultiRNNCell(cells,state_is_tuple=True)
'''
outputs, _states = tf.nn.dynamic_rnn(cell, X, dtype=tf.float32)
Y_pred = tf.contrib.layers.fully_connected(outputs[:,-1], output_dim, activation_fn=None)

targets = tf.placeholder(tf.float32, [None, data_dim])
predictions = tf.placeholder(tf.float32, [None, data_dim])
rmse = tf.sqrt(tf.reduce_mean(tf.square(targets - predictions)))

sess=tf.Session()
saver=tf.train.Saver()

init = tf.global_variables_initializer()
sess.run(init)

save_path="./rnn_train_co2.ckpt"
saver.restore(sess,save_path)  # restore train variable

# Test step
test_predict = sess.run(Y_pred, feed_dict={X: testX})

# 5 times added prediction
temp_list=testX[-1]
temp_list=np.delete(temp_list, 0, axis=0)
temp_list= np.append(temp_list, xy[-1, 0].reshape(1, 1), axis=0)
test_predict1 = sess.run(Y_pred, feed_dict={X: temp_list.reshape(1, 7, 1)})
temp_list=np.delete(temp_list, 0,axis=0)
temp_list= np.append(temp_list, test_predict[-1, 0].reshape(1, 1), axis=0)
test_predict2 = sess.run(Y_pred, feed_dict={X: temp_list.reshape(1, 7, 1)})
temp_list=np.delete(temp_list, 0,axis=0)
temp_list= np.append(temp_list, test_predict[-1, 0].reshape(1, 1), axis=0)
test_predict3 = sess.run(Y_pred, feed_dict={X: temp_list.reshape(1, 7, 1)})
temp_list=np.delete(temp_list, 0,axis=0)
temp_list= np.append(temp_list, test_predict[-1, 0].reshape(1, 1), axis=0)
test_predict4 = sess.run(Y_pred, feed_dict={X: temp_list.reshape(1, 7, 1)})
temp_list=np.delete(temp_list, 0,axis=0)
temp_list= np.append(temp_list, test_predict[-1, 0].reshape(1, 1), axis=0)
test_predict5 = sess.run(Y_pred, feed_dict={X: temp_list.reshape(1, 7, 1)})

rmse_val = sess.run(rmse, feed_dict={targets: testY, predictions: test_predict})
print("RMSE: {}".format(rmse_val))

test_predict=np.append(test_predict, test_predict1, axis=0)
test_predict=np.append(test_predict, test_predict2, axis=0)
test_predict=np.append(test_predict, test_predict3, axis=0)
test_predict=np.append(test_predict, test_predict4, axis=0)
test_predict=np.append(test_predict, test_predict5, axis=0)

testY = testY*( np.max(xy1, 0) - np.min(xy1, 0) + 1e-7)+np.min(xy1, 0)  # Decode MinMaxScalar
test_predict = test_predict*(np.max(xy1, 0) - np.min(xy1, 0) + 1e-7)+np.min(xy1, 0)


f='%Y-%m-%d %H:%M:%S'  # time format
list_length=len(testY)


# delete last 5 data
cursor.execute("DELETE FROM predict_co2 WHERE value1 is null")
# delete more than 4 hours ago
cursor.execute("DELETE FROM predict_co2 WHERE time < '" + str(datetime.datetime.now()-datetime.timedelta(hours=4)) + "'")
con.commit()

# save db
cursor.execute("INSERT INTO predict_co2 (value1,value2) VALUES (%f,%f)"
               % (testY[list_length-1], test_predict[list_length-1]))
for i in range(5):
    cursor.execute("INSERT INTO predict_co2 (value2,time) VALUES (%f,'%s')"
                   % (test_predict[list_length+i],
                      datetime.datetime.strptime(str(last_time[0]), f) + datetime.timedelta(minutes=i+1)))
con.commit()

cursor.close()
con.close()  # db disconnect

#loop on pm2