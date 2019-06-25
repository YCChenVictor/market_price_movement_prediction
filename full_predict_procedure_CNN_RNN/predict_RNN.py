import tensorflow as tf
import numpy as np
import os
import pickle
import json
import functions.about_path as fap
# import sys
# import numpy
# numpy.set_printoptions(threshold=sys.maxsize)

# import prerequisite
file_path = os.path.dirname(os.path.realpath(__file__))
parent_path = fap.f_parent_path(file_path)
path = parent_path + '/docs/' + 'Prerequisite.json'
with open(path) as f:
    prerequisite = json.load(f)

batch_size = prerequisite["batch_size"]
predict_target = prerequisite["predict_target"]


# delete the current graph
tf.reset_default_graph()


# the data to make prediction
file_path = os.path.dirname(os.path.realpath(__file__))

roll_conn_flat_test_path = file_path + '/docs/' + 'roll_conn_flat_test.pickle'
with open(roll_conn_flat_test_path, 'rb') as f:
    roll_conn_flat_test = pickle.load(f)

move_path = file_path + '/docs/' + 'movement.pickle'
with open(move_path, 'rb') as f:
    movement = pickle.load(f)

# movement dict
movement_target = movement[predict_target]
movement_dict = movement_target.to_dict()


with tf.Session() as sess:

    # use import_meta_graph
    last_ckp = tf.train.latest_checkpoint("./model_RNN")
    imported_graph = tf.train.import_meta_graph(last_ckp + '.meta')
    imported_graph.restore(sess, last_ckp)
    print("Model restored.")

    # get the saved data
    x = tf.get_collection('input')[0]
    y = tf.get_collection('output')[0]
    keep_prob = tf.get_collection('keep_prob')[0]

    accuracy_list = []

    # test prediction ####
    for key, item in roll_conn_flat_test.items():

        # make it as batch_size
        test_data = np.tile(item, (batch_size, 1))

        # make prediction
        result = sess.run(y, feed_dict={x: np.reshape(test_data,
                                                      (-1, item.shape[0],
                                                       item.shape[1])),
                                        keep_prob: 1.0})
        target = movement_dict[key]
        predict = sum(result)/len(result)

        print("true movement in ", key, ": ", target)
        print("prediction: ", predict)
        print("======================")

        # calculate accuracy
        if predict == target:
            accuracy_list.append(1)
        else:
            accuracy_list.append(0)

    # calculate accuracy
    accuracy = sum(accuracy_list)/len(accuracy_list)
    print("prediction accuracy:", accuracy)
