import pandas as pd
import pickle
from .model_base import BasePredictionModel
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score

class ClientPredictionModel(BasePredictionModel):

    def __init__(self,model_pickle=None):
        if model_pickle:
            super().__init__(model_pickle)
        else:
            model_params = {
                'class_weight': {1:1.1, 0:1}
                }
            self.model = GridSearchCV(
                estimator=ExtraTreesClassifier(**model_params),
                param_grid={'max_depth':[3,5], 'n_estimators':[50,100,200]},
                cv=5,
                scoring='f1'
                )
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

        if y.value_counts().nunique() < 2:
            raise Exception("Error: Only one target class represented in training data.")
        if y.value_counts()[1] < 0.2*len(y):
            print("Balancing classes...")
            X, y = SMOTE().fit_sample(X, y)

        # Train the model here.
        self.model.fit(X,y)
        self.model = self.model.best_estimator_
        self.model_params = dict(self.model.get_params())
        self.is_trained = True
        print("Model trained.")


    def predict(self,prediction_data,predictors):
        super().predict()
        xp = prediction_data[predictors]
        return self.model.predict(xp)


    def predict_probabilities(self,prediction_data,predictors):
        super().predict()
        xp = prediction_data[predictors]
        return self.model.predict_proba(xp)


    def validate(self,validation_data,predictors,target):
        super().validate()
        if target in predictors:
            raise Exception("Error: Target cannot also be a predictor")

        xv,yv = validation_data[predictors], validation_data[target]
        yp = self.predict(xv,predictors)
        test_set_size = len(yp)

        true_negatives, false_positives, false_negatives, true_positives = confusion_matrix(yv,yp).ravel()
        accuracy, recall, precision = 0, 0, 0
        if len(yp) != 0:
            accuracy = (true_positives + true_negatives) / len(yp)
        if (true_positives + false_negatives) != 0:
            recall = true_positives / (true_positives + false_negatives)
        if (true_positives + false_negatives) != 0:
            precision = true_positives / (true_positives + false_positives)
        yp_prob = [p[1] for p in self.predict_probabilities(xv,predictors)]
        return {"test_set_size": test_set_size, "recall": recall, "precision": precision, "accuracy": accuracy, "roc_auc_score": roc_auc_score(yv,yp_prob)}
