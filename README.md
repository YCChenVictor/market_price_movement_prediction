# Market Price Movement Prediction

## Usage
```bash
python3 main.py
```

## data flow

* Get Open, Close, High, Low, data
* Calculate volatilities -> store into database
* Calculate connectedness -> store into database
* Prediction

## Development Conclusion

* CNN cannot be used (training accuracy cannot increase)
* LSTM can still be used (training accuracy can reach 100%)
* Convert CNN_LSTM to ConvLSTM
