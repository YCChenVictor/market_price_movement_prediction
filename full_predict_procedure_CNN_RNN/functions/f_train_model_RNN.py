import tensorflow as tf
import json


# tfrecords
def read_and_decode(filename, batch_size, num_of_epoches,
                    conns_for_one_element, n_table_elements):

    # produce the file queue
    filename_queue = tf.train.string_input_producer([filename],
                                                    shuffle=True,
                                                    num_epochs=num_of_epoches)
    '''
    because there is only one file, TF record file, the shuffle=True won't
    work. Shuffle one file is still the same!
    '''

    # The tool to read data from Train.tfrecords
    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_queue)

    # unpack tfrecords
    '''
    The steps in packing TFRecord file:
    original file > Feature > Features > Example > TFRecord

    The steps in unpacking TFRecord file:
    TFRecord > Example > Features > Feature > original file

    Use tf.parse_single_example to turn tf.train.Example into
    tf.train.Features

    Use tf.decode_raw or tf.cast to turn tf.train.qFeatures into
    tf.train.Feature
    '''
    features = {'output': tf.FixedLenFeature([], tf.int64),
                'input': tf.FixedLenFeature([], tf.string)}
    data_features = tf.parse_single_example(serialized_example,
                                            features=features)

    input_tensor = tf.decode_raw(data_features['input'], tf.float32)
    input_tensor = tf.reshape(input_tensor, [conns_for_one_element,
                                             n_table_elements])

    output_tensor = tf.cast(data_features['output'], tf.int64)

    # output data in order / output data in random
    # tf.train.batch / tf.train.shuffle_batch
    input_batch, output_batch = tf.train.shuffle_batch(
        [input_tensor, output_tensor],
        batch_size=batch_size,
        capacity=10000 + 3 * batch_size,
        min_after_dequeue=1000
        )

    return input_batch, output_batch

    # parameters of tf.train.shuffle_batch:
    # tensor: input_tensor and output_tensor
    # batch_size：The number of elements in a batch
    # capacity: must be int, the maximum number of element
    # min_after_dequeue： must be int, the minimum number remained after output
    # all the data


# function to train multi-layer RNN
def neural_network_model(x, layer_num, n_hidden_units, batch_size,
                         label_size, n_table_elements, conns_for_one_element,
                         keep_prob):

    # define weight & biases for x and y
    weights = {
        'in': tf.Variable(tf.random_normal([n_table_elements,
                                            n_hidden_units])),
        'out': tf.Variable(tf.random_normal([n_hidden_units, label_size]))
    }
    biases = {
        'in': tf.Variable(tf.constant(0.1, shape=[n_hidden_units, ])),
        # shape (10, )
        'out': tf.Variable(tf.constant(0.1, shape=[label_size, ]))
    }

    # original x shape is 3 dimension. we need to transform into 2 dimension to
    # //input the data into weight
    x_in = tf.reshape(x, [-1, n_table_elements])

    # step_1: the input data shape = [batch_size, timestep_size, input_size]
    x_in = tf.matmul(x_in, weights['in']) + biases['in']
    x_in = tf.reshape(x_in, [-1, conns_for_one_element, n_hidden_units])

    # step_2: define one layer lstm_cell, only needs to explain hidden_size
    lstm_cell = tf.contrib.rnn.BasicLSTMCell(num_units=n_hidden_units,
                                             forget_bias=1.0,
                                             state_is_tuple=True)

    # step_3: add dropout layer as regularization
    lstm_cell = tf.contrib.rnn.DropoutWrapper(cell=lstm_cell,
                                              input_keep_prob=1.0,
                                              output_keep_prob=keep_prob)

    # step_4: construct nulti-layer LSTM
    mlstm_cell = tf.nn.rnn_cell.MultiRNNCell([lstm_cell for _ in
                                              range(layer_num)])

    # step_5: initialize state
    init_state = mlstm_cell.zero_state(batch_size, dtype=tf.float32)

    # step_6: use dynamic_rnn to get the output and state
    outputs, state = tf.nn.dynamic_rnn(mlstm_cell, inputs=x_in,
                                       initial_state=init_state,
                                       time_major=False)
    h_state = outputs[:, -1, :]
    # print("h_state shape")
    # print(h_state)
    '''
    when time_major==False, outputs.shape = [batch_size, timestep_size,
                                             hidden_size],
    we can use h_state = outputs[:, -1, :] as last output
    '''

    y = tf.nn.softmax(tf.matmul(h_state, weights['out']) + biases['out'])

    return y


def train_RNN(coord, sess, train_x, train_y, optimizer, x, y_, accuracy,
              saver, save_path, count_save_path, count, loss, keep_prob):

    try:
        while not coord.should_stop():

            input_data, output_data = sess.run([train_x, train_y])

            # print(input_data)
            # print(output_data)

            # start training
            sess.run(optimizer, feed_dict={x: input_data,
                                           y_: output_data,
                                           keep_prob: 0.5})

            # print(count)
            # print out accuracy
            if count % 50 == 0:

                # calculate accuracy
                train_accuracy = accuracy.eval({x: input_data,
                                                y_: output_data,
                                                keep_prob: 1.0})

                # calculate loss
                train_cost = loss.eval({x: input_data,
                                        y_: output_data,
                                        keep_prob: 1.0})

                # print out accuracy
                print('Iter %d, accuracy %4.2f%%' % (count,
                                                     train_accuracy*100))
                print('Iter %d, loss %f' % (count, train_cost))
                print("=========================")

                # save all the session
                spath = saver.save(sess, save_path, global_step=count)
                print("Model saved in file: %s" % spath)

                # save the count
                path = count_save_path

                with open(path) as f:
                    Post_requisite = json.load(f)

                Post_requisite["train_time"] = count

                with open(path, 'w') as outfile:
                    json.dump(Post_requisite, outfile)

            count = count + 1

    # If num_epochs run out => error
    except tf.errors.OutOfRangeError:
        print("---Train end---")

    finally:
        # terminate coord
        coord.request_stop()
        print('---Programm end---')
        # addd the trained line to threads
