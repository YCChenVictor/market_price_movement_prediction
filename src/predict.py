import tensorflow as tf
import numpy as np
import argparse

model = tf.keras.models.load_model('model.keras')
print(model.)
input_data = np.random.random((1, 5, 64))
predictions = model.predict(input_data)
print(predictions)

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description="Script with other variables")
#     parser.add_argument('--predict_ticker', type=str, help="Ticker to predict the movement")
#     parser.add_argument('--timestamp', type=str, help="Timestamp to predict the movement")
#     args = parser.parse_args()
#     predict_ticker = args.predict_ticker
#     timestamp = args.timestamp


      # scrape the require data again
      
      # calculate calculate the connectedness
      # feed connectedness into the model

      # I need to know the correct input for prediction, what's the correct shape?

#     # return the prediction

