"""
should specify what periods we predicting
"""

import tensorflow as tf
from tensorflow.python.ops import rnn, rnn_cell
import numpy as np
import pickle


# define function to split dataset into train and predict
def train_predict_split(inputs_outputs_dict, predict_periods=1):

    # create train and test dict
    train_dict = {}
    test_dict = {}

    key_list = list(inputs_outputs_dict.keys())

    train_key_list = key_list[:-predict_periods]
    test_key_list = key_list[(len(key_list)-predict_periods):len(key_list)]

    for key in train_key_list:
        train_dict[key] = inputs_outputs_dict[key]

    for key in test_key_list:
        test_dict[key] = inputs_outputs_dict[key]

    return train_dict, test_dict


# define function to make prediction
def recurrent_neural_network(x, chunk_size, n_chunks, rnn_size, layer):

    # reshape the data into whatever x chunk size and then split it into
    # //timeseries inputs
    x = tf.reshape(x, [-1, chunk_size])
    x = tf.split(x, n_chunks, 0)

    lstm_cell = rnn_cell.MultiRNNCell([rnn_cell.BasicLSTMCell(rnn_size),
                                       rnn_cell.BasicLSTMCell(rnn_size)])

    outputs, states = rnn.static_rnn(lstm_cell, x, dtype=tf.float32)

    output = tf.matmul(outputs[-1], layer['weights']) + layer['biases']

    return output


# define function to train model
def train_neural_network(x, y, tf_log, hm_epochs, saver, train_dict,
                         chunk_size, n_chunks, rnn_size, layer, save_path):

    # define required tensors
    prediction = recurrent_neural_network(x, chunk_size, n_chunks, rnn_size,
                                          layer)
    cost = tf.reduce_mean(tf.square(prediction - y))
    optimizer = tf.train.AdamOptimizer().minimize(cost)

    # start session
    with tf.Session() as sess:

        sess.run(tf.global_variables_initializer())

        # training
        epoch = 1

        epoch_list = []

        while epoch <= hm_epochs:

            print("Start to train epoch %d" % epoch)
            print("========================")

            epoch_loss = 0

            for key, item in train_dict.items():

                # get input and output
                input_data = item[0].tail(n_chunks)
                output_data = item[1]

                # do the training
                epoch_x = np.array(input_data)
                # print(epoch_x)
                epoch_y = np.asarray(output_data)
                # print(epoch_y)

                # start to train
                _, c = sess.run([optimizer, cost],
                                feed_dict={x: epoch_x, y: epoch_y})
                # print(c)
                epoch_loss += c
                # print(epoch_loss)

                # if epoch_loss < 10:
                #     break

            # make prediction to train set
            accuracy_list = []

            for key, item in train_dict.items():

                input_data = item[0].tail(n_chunks)

                output_data = item[1]

                predict_x = np.array(input_data)

                prediction_value = prediction.eval({x: predict_x})

                if prediction_value > 0:
                    prediction_bin = "up"
                else:
                    prediction_bin = "down"

                if output_data > 0:
                    real_bin = "up"
                else:
                    real_bin = "down"

                # the accuracy
                if prediction_bin == real_bin:
                    accuracy_list.append(1)
                else:
                    accuracy_list.append(0)

                # print('predict_value:', prediction_value)
                # print('predict_bin', prediction_bin)
                # print('true_bin', output_data)

            print("==============")

            accuracy = sum(accuracy_list)/len(accuracy_list)

            print('the accuracy: ', accuracy)

            # save the trained session
            saver.save(sess, "check_point/model.ckpt")

            print('Epoch', epoch, 'completed out of', hm_epochs,
                  'loss:', epoch_loss)
            print("===========================================")

            with open(tf_log, 'a') as f:
                f.write(str(epoch)+'\n')

            epoch += 1

            # save the loss
            epoch_list.append(epoch_loss)
            with open(save_path, 'wb') as f:
                pickle.dump(epoch_list, f)

            # print(epoch_list)

            if accuracy > 0.9:
                break


# use the function trained in train_neural_network() to make prediction with //
# predict dataset
def predict_neural_network(x, y, chunk_size, n_chunks, rnn_size, layer,
                           hm_epochs, saver, predict_set):
    """
    should make sure whether it load the trained model accurately
    """

    tf.get_variable_scope().reuse_variables()

    prediction = recurrent_neural_network(x, chunk_size, n_chunks, rnn_size,
                                          layer)

    with tf.Session() as sess:

        sess.run(tf.global_variables_initializer())

        for epoch in range(hm_epochs):
            try:
                saver.restore(sess, "check_point/model.ckpt")
            except Exception as e:
                print(str(e))

        # make prediction
        accuracy_list = []

        for key, item in predict_set.items():

            input_data = item[0].tail(n_chunks)

            output_data = item[1]

            predict_x = np.array(input_data)

            prediction_value = prediction.eval({x: predict_x})

            if prediction_value > 0:
                prediction_bin = "up"
            else:
                prediction_bin = "down"

            if output_data > 0:
                real_bin = "up"
            else:
                real_bin = "down"

            # the accuracy
            if prediction_bin == real_bin:
                accuracy_list.append(1)
            else:
                accuracy_list.append(0)

            print('predict_value:', prediction_value)
            print('predict_bin', prediction_bin)
            print('true_bin', output_data)

        print("==============")

        accuracy = sum(accuracy_list)/len(accuracy_list)
        print('the accuracy: ', accuracy)
