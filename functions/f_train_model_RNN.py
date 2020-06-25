import tensorflow as tf
import json
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

# tfrecords (放棄，不使用tfrecord)
'''https://ithelp.ithome.com.tw/articles/10214280?sc=hot'''
def extract_features(example, conns_for_one_element, n_table_elements):

    features = tf.io.parse_single_example(
        example,
        features={
            'output': tf.io.FixedLenFeature([], tf.string), # label
            'input': tf.io.FixedLenFeature([], tf.string) # matrix, string type
        }
    )
    input_tensor = tf.io.decode_raw(features['input'], tf.float32)
    input_tensor = tf.reshape(input_tensor, [conns_for_one_element, n_table_elements])
    input_tensor = tf.cast(input_tensor, tf.float32)
    input_tensor = tf.expand_dims(input_tensor, -1)
    output_tensor = tf.io.decode_raw(features['output'], tf.float32)
    output_tensor = tf.reshape(output_tensor, [1])
    output_tensor = tf.cast(output_tensor, tf.float32)
    return input_tensor, output_tensor

# batched dataset (放棄，不使用tfrecord)
def get_batched_dataset(filenames, conns_for_one_element, n_table_elements, batch_size):
    option_no_order = tf.data.Options()
    option_no_order.experimental_deterministic = False

    dataset = tf.data.Dataset.list_files(filenames)
    dataset = dataset.with_options(option_no_order)
    dataset = dataset.interleave(tf.data.TFRecordDataset, cycle_length=16)
    dataset = dataset.map(lambda x: extract_features(x, conns_for_one_element, n_table_elements))

    dataset = dataset.cache() # This dataset fits in RAM
    dataset = dataset.repeat()
    dataset = dataset.shuffle(2048)
    dataset = dataset.batch(batch_size, drop_remainder=True)

    return dataset

# step to build training model structure
def get_model(conns_for_one_element, n_table_elements, n_hidden_units):
    model = Sequential()

    model.add(LSTM(units = n_table_elements, return_sequences = True, input_shape = (conns_for_one_element, n_table_elements)))
    model.add(Dropout(0.2))

    model.add(LSTM(units = n_table_elements, return_sequences = True))
    model.add(Dropout(0.2))

    model.add(LSTM(units = n_hidden_units, return_sequences = False))
    model.add(Dense(units = n_hidden_units/2))
    model.add(Dense(units = n_hidden_units/4))
    model.add(Dense(units = 1))
    model.compile(optimizer = 'adam', loss = 'mean_squared_error', metrics=['accuracy'])

    return model
