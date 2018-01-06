import tensorflow as tf
import numpy as np
from tensorflow.contrib import rnn

sentence = ("""That, poor contempt, or claim'd thou slept so faithful, I may contrive our father; and, in their defeated queen, Her flesh broke me and puttance of expedition house, And in that same that ever I lament this stomach, And he, nor Butly and my fury, knowing everything Grew daily ever, his great strength and thought The bright buds of mine own.

BIONDELLO:
Marry, that it may not pray their patience.'

KING LEAR:
The instant common maid, as we may less be a brave gentleman and joiner: he that finds us with wax And owe so full of presence and our fooder at our staves. It is remorsed the bridal's man his grace for every business in my tongue, but I was thinking that he contends, he hath respected thee.

BIRON:
She left thee on, I'll die to blessed and most reasonable Nature in this honour, and her bosom is safe, some others from his speedy-birth, a bill and as Forestem with Richard in your heart Be question'd on, nor that I was enough: Which of a partier forth the obsers d'punish'd the hate To my restraints would not then be got as I partly.

AUTOLYCUS:
Hath sat her love within this man, that was foul prayers Which are much thus from them with thee; I am not ever thought To make that with a wise exclaim, as I am sure; To say well like a dotage on the fixed cease, And let mine eyes may straight sole sword conveyard, That dust-confounded by a land to their command Then puissant with a grief's: it should be so and dead, Till he shall fail his sister; and in true and good, To see me for the other, hath not heard a midwife Loud from my service and thy sweetly daughter got The single strange words pent is all his steed: Stay from us in, as he hath we brought me into the Milthiness."""         
               )

char_set = list(set(sentence))
char_dic = {w: i for i, w in enumerate(char_set)}

data_dim = len(char_set)
hidden_size = len(char_set)
num_classes = len(char_set)
seq_length = 30  # Any arbitrary number

dataX = []
dataY = []
for i in range(0, len(sentence) - seq_length):
    x_str = sentence[i:i + seq_length]
    y_str = sentence[i + 1: i + seq_length + 1]
    print(i, x_str, '->', y_str)

    x = [char_dic[c] for c in x_str]  # x str to index
    y = [char_dic[c] for c in y_str]  # y str to index

    dataX.append(x)
    dataY.append(y)

batch_size = len(dataX)

X = tf.placeholder(tf.int32, [None, seq_length])
Y = tf.placeholder(tf.int32, [None, seq_length])

X_one_hot = tf.one_hot(X, num_classes)
print(X_one_hot)  # check out the shape

cell = rnn.BasicLSTMCell(hidden_size)
rnn_cell = rnn.MultiRNNCell([cell] * 3, state_is_tuple=True)

outputs, _states = tf.nn.dynamic_rnn(cell, X_one_hot, dtype=tf.float32)

X_for_softmax = tf.reshape(outputs, [-1, hidden_size])
softmax_w = tf.get_variable("softmax_w", [hidden_size, num_classes])
softmax_b = tf.get_variable("softmax_b", [num_classes])
outputs = tf.matmul(X_for_softmax, softmax_w) + softmax_b

# reshape out for sequence_loss
outputs = tf.reshape(outputs, [batch_size, seq_length, num_classes])
# All weights are 1 (equal weights)
weights = tf.ones([batch_size, seq_length])

sequence_loss = tf.contrib.seq2seq.sequence_loss(logits=outputs, targets=Y, weights=weights)
mean_loss = tf.reduce_mean(sequence_loss)
train_op = tf.train.AdamOptimizer(learning_rate=0.1).minimize(mean_loss)

sess = tf.Session()
sess.run(tf.global_variables_initializer())
for i in range(500):
    _, l, results = sess.run([train_op, mean_loss, outputs], feed_dict={X: dataX, Y: dataY})
    for j, result in enumerate(results):
        index = np.argmax(result, axis=1)
        print(i, j, ''.join([char_set[t] for t in index]), l)
        
# Let's print the last char of each result to check it works
results = sess.run(outputs, feed_dict={X: dataX})
for j, result in enumerate(results):
    index = np.argmax(result, axis=1)
    if j is 0:  # print all for the first result to make a sentence
        print ("".join([char_set[t] for t in index]))
    else:
        print (char_set[index[-1]])
