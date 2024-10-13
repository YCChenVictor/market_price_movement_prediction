import json
import tensorflow as tf
import numpy as np
import argparse
from scrape_finance_data_yahoo import scrape_and_save_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script with other variables")
    parser.add_argument('--predict_ticker', type=str, help="Ticker to predict the movement")
    parser.add_argument('--timestamp', type=str, help="Timestamp to predict the movement")
    args = parser.parse_args()
    predict_ticker = args.predict_ticker
    timestamp = args.timestamp

    with open('docs/trained_model_metadata.json', 'r') as f:
        metadata = json.load(f)
    model = tf.keras.models.load_model(metadata['model_path'])
    scrape_and_save_data(metadata['feature_tickers'], 'docs/market_prices/predict')
    # print(model.input_shape)
    # steps = model.input_shape[1]
    # input_data = np.random.random((1, 5, 64))
    # predictions = model.predict(input_data)
    # print(predictions)


      # scrape the require data again
      
      # calculate calculate the connectedness
      # feed connectedness into the model

      # I need to know the correct input for prediction, what's the correct shape?

#     # return the prediction

