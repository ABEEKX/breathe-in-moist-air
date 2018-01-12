import tensorflow as tf
import numpy as np
import pymysql

tf.set_random_seed(700)

seq_length = 7
data_dim = 1
hidden_dim = 10
output_dim = 1
learning_rate = 0.01
iterations = 1000
#num_layers = 3

# connect db
con=pymysql.connect(host='52.78.192.119',port=3306,user='root',password='Cap2bowoo!',db='abeekx',charset='utf8')
cursor=con.cursor()
cursor.execute("SELECT temp,time FROM sensors")

xy=[]
for row in cursor:
    xy.append([float(row[0])])

cursor.close()
con.close()  # db disconnect

xy1=xy  # pre Scalar data
numerator = xy - np.min(xy, 0)  # MinMaxScalar
denominator = np.max(xy, 0) - np.min(xy, 0)
xy =  (xy - np.min(xy, 0))/ (denominator + 1e-7)
x = xy

dataX = []
dataY = []
for i in range(0, len(x) - seq_length):
    _x = x[i:i + seq_length]
    _y = x[i+seq_length]
    dataX.append(_x)
    dataY.append(_y)

# train/test split
train_size = int(0.8*len(dataX))
trainX, testX = np.array(dataX[0:train_size]), np.array(dataX[train_size:len(dataX)])
trainY, testY = np.array(dataY[0:train_size]), np.array(dataY[train_size:len(dataY)])

# input place holders
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
cell = tf.contrib.rnn.MultiRNNCell(cells,state_is_tuple=True)'''
outputs, _states = tf.nn.dynamic_rnn(cell, X, dtype=tf.float32)
Y_pred = tf.contrib.layers.fully_connected(outputs[:,-1], output_dim, activation_fn=None)

# cost/loss
loss = tf.reduce_sum(tf.square(Y_pred - Y))  # sum of the squares
# optimizer
optimizer = tf.train.AdamOptimizer(learning_rate)
train = optimizer.minimize(loss)

# RMSE
targets = tf.placeholder(tf.float32, [None, data_dim])
predictions = tf.placeholder(tf.float32, [None, data_dim])
rmse = tf.sqrt(tf.reduce_mean(tf.square(targets - predictions)))

sess=tf.Session()
init = tf.global_variables_initializer()
sess.run(init)
# Training step
for i in range(iterations):
    _, step_loss = sess.run([train, loss], feed_dict={X: trainX, Y: trainY})
    print("[step: {}] loss: {}".format(i, step_loss))

saver=tf.train.Saver()
save_path=saver.save(sess,"./rnn_train.ckpt")  # save train variable
