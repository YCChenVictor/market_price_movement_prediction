import numpy as np

class ModelTrainer:
    def __init__(self, target, features): 
        self.target = target
        self.features = features
        self.match_target_features = None

    def match(self, steps):
        print("matching")
        # you need to divide it into several steps,
        # I think you should have key, timestamp items, [steps, movement]
        match_target_features = {}
        start_index = 0
        end_index = steps
        forecast_row_index = 0
        while(forecast_row_index < len(self.features)):
            current_features = self.features.iloc[start_index:end_index]
            forecast_row_index = end_index - 1 + current_features.iloc[-1]["forecast_at"]
            forecast_at_time = self.features.loc[forecast_row_index]["end_at"]
            target_movement = self.target[self.target["Time"] == forecast_at_time] # this is O(n), try to make it as O(1)
            match_target_features[forecast_at_time] = [target_movement, current_features]
            start_index += 1
            end_index += 1
            forecast_row_index += 1
        self.match_target_features = match_target_features

    def train(self):
        X_train = np.random.rand(100, 10, 3)
        y_train = np.random.randint(0, 2, size=(100, 1))
        print(X_train[0])
        print(y_train[0])
        print(self.features)
        print(self.target)
        # self.model.fit(self.features, self.target, epochs=epochs, batch_size=batch_size)
