import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os
import pymysql


tf.set_random_seed(700)

if "DISPLAY" not in os.environ:
    # remove Travis CI Error
    matplotlib.use('Agg')


def MinMaxScaler(data):
    #  Min Max Normalization
    numerator = data - np.min(data, 0)
    denominator = np.max(data, 0) - np.min(data, 0)
    # noise term prevents the zero division
    return numerator / (denominator + 1e-7)

seq_length = 7
data_dim = 1
hidden_dim = 10
output_dim = 1
learning_rate = 0.01
iterations = 500

# connect db
con=pymysql.connect(host='52.78.192.119',port=3306,user='root',password='Cap2bowoo!',db='abeekx',charset='utf8')
cursor=con.cursor()
cursor.execute("SELECT temp FROM sensors")
xy=[]
for row in cursor:
    xy.append([float(row[0])])

cursor.close()
con.close()  # db disconnect

xy=xy[::-1]  # reverse data
xy1=xy  # pre Scalar data
numerator = xy - np.min(xy, 0)  # MinMaxScalar
denominator = np.max(xy, 0) - np.min(xy, 0)
xy =  (xy - np.min(xy, 0))/ (denominator + 1e-7)
x = xy
y = xy[:,[-1]]  # Close as label

dataX = []
dataY = []
for i in range(0, len(y) - seq_length):
    _x = x[i:i + seq_length]
    _y = y[i + seq_length]  # Next temperature
    dataX.append(_x)
    dataY.append(_y)

# train/test split
train_size = int(len(dataY) * 0.7)
test_size = len(dataY) - train_size
trainX, testX = np.array(dataX[0:train_size]), np.array(
    dataX[train_size:len(dataX)])
trainY, testY = np.array(dataY[0:train_size]), np.array(
    dataY[train_size:len(dataY)])

# input place holders
X = tf.placeholder(tf.float32, [None, seq_length, data_dim])
Y = tf.placeholder(tf.float32, [None, 1])

# build a LSTM network
cell = tf.contrib.rnn.BasicLSTMCell(
    num_units=hidden_dim, state_is_tuple=True, activation=tf.tanh)
outputs, _states = tf.nn.dynamic_rnn(cell, X, dtype=tf.float32)
Y_pred = tf.contrib.layers.fully_connected(
    outputs[:,-1], output_dim, activation_fn=None)  # reverse output

# cost/loss
loss = tf.reduce_sum(tf.square(Y_pred - Y))  # sum of the squares
# optimizer
optimizer = tf.train.AdamOptimizer(learning_rate)
train = optimizer.minimize(loss)

# RMSE
targets = tf.placeholder(tf.float32, [None, 1])
predictions = tf.placeholder(tf.float32, [None, 1])
rmse = tf.sqrt(tf.reduce_mean(tf.square(targets - predictions)))

with tf.Session() as sess:
    init = tf.global_variables_initializer()
    sess.run(init)
    # Training step
    for i in range(iterations):
        _, step_loss = sess.run([train, loss], feed_dict={X: trainX, Y: trainY})
        print("[step: {}] loss: {}".format(i, step_loss))

    # Test step
    test_predict = sess.run(Y_pred, feed_dict={X: testX})
    rmse_val = sess.run(rmse, feed_dict={
                    targets: testY, predictions: test_predict})
    print("RMSE: {}".format(rmse_val))

    # Plot predictions
    testY = testY*( np.max(xy1, 0) - np.min(xy1, 0) + 1e-7)+np.min(xy1, 0)  # Decode MinMaxScalar
    plt.plot(testY)
    # 4 times added prediction
    distance=(test_predict[-1]-test_predict[-2])*0.2  # Momentum
    for i in range(5):
        test_predict=np.append(test_predict,[test_predict[-1]+(i+1)*distance],axis=0)

    test_predict=test_predict*( np.max(xy1, 0) - np.min(xy1, 0) + 1e-7)+np.min(xy1, 0)  # Decode MinMaxScalar
    plt.plot(test_predict)
    plt.xlabel("Time Period")
    plt.ylabel("Temperature")
    plt.show()