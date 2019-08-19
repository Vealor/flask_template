import pandas as pd
import pickle
from .model_base import BasePredictionModel
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report

class MasterPredictionModel(BasePredictionModel):

    def __init__(self,model_pickle=None):
        if model_pickle:
            super().__init__(model_pickle)
        else:
            model_params = {
                'n_estimators': 100,
                'max_depth': 5,
                'random_state': 42,
                'class_weight': {1:1.1, 0:1}
                }
            self.model = RandomForestClassifier(**model_params)
            self.is_trained = False


    def train(self,training_data,predictors,target):
        super().train()

        # Check if target variable is also in predictors
        if target in predictors:
            raise Exception("Error: Target cannot also be a predictor")

        # Perform additional training preprocessing here.
        # If there is a significant class imbalance, do some synthetic over_sampling
        X = training_data[predictors]
        y = training_data[target]
        if y.value_counts()[1] < 0.2*len(y):
            print("Balancing classes...")
            X, y = SMOTE().fit_sample(X, y)

        # Train the model here.
        self.model.fit(X,y)
        self.is_trained = True
        print("Model trained.")


    def predict(self,prediction_data,predictors):
        super().predict()
        xp = prediction_data[predictors]
        return self.model.predict(xp)


    def validate(self,validation_data,predictors,target):
        super().validate()
        if target in predictors:
            raise Exception("Error: Target cannot also be a predictor")

        xv,yv = validation_data[predictors], validation_data[target]
        yp = self.predict(xv,predictors)

        true_negatives, false_positives, false_negatives, true_positives = confusion_matrix(yv,yp).ravel()
        accuracy, recall, precision = 0, 0, 0
        if len(yp) != 0:
            accuracy = (true_positives + true_negatives) / len(yp)
        if (true_positives + false_negatives) != 0:
            recall = true_positives / (true_positives + false_negatives)
        if (true_positives + false_negatives) != 0:
            precision = true_positives / (true_positives + false_positives)

        return {"recall": recall, "precision": precision, "accuracy": accuracy}