import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
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
cursor.execute("SELECT MAX(id) FROM sensors")  # check new data in
for row in cursor:
    pre_max_id = int(row[0])

cursor.execute("SELECT temp,time FROM sensors")
xy=[]
time=[]
for row in cursor:
    xy.append([float(row[0])])
    time.append([str(row[1])])  # get timestamp

#xy=xy[::-1]  # reverse data
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
train_size = int(0.9*len(dataX))
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

save_path="./rnn_train.ckpt"
saver.restore(sess,save_path)  # restore train variable

# Test step
test_predict = sess.run(Y_pred, feed_dict={X: testX})

# 5 times added prediction
temp_list=testX[-1]
temp_list=np.delete(temp_list, 0, axis=0)
temp_list= np.append(temp_list, test_predict[-1, 0].reshape(1, 1), axis=0)
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

cursor.execute("SELECT MAX(id) FROM sensors")  # check new data in
for row in cursor:
    max_id=float(row[0])

if(max_id != pre_max_id):
    # delete last 5 data
    cursor.execute("DELETE FROM predict WHERE value1 is null")
    con.commit()

    # save db
    cursor.execute("INSERT INTO predict (value1,value2) VALUES (%f,%f)"
                   % (testY[list_length-1], test_predict[list_length-1]))
    for i in range(5):
        cursor.execute("INSERT INTO predict (value2,time) VALUES (%f,'%s')"
                       % (test_predict[list_length+i],
                          datetime.datetime.strptime(str(timeY[-1, 0]), f) + datetime.timedelta(minutes=i+1)))
    con.commit()

cursor.close()
con.close()  # db disconnect

#loop on pm2