import pandas as pd
import pickle
from .model_base import BasePredictionModel
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import RandomizedSearchCV
from lightgbm import LGBMClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score, fbeta_score, make_scorer
from scipy.stats import poisson

class MasterPredictionModel_EXP(BasePredictionModel):

    def __init__(self,model_pickle=None):
        if model_pickle:
            super().__init__(model_pickle)
        else:
            # Define the master model here.
            model_params = {'boosting_type': 'gbdt', 'forcedsplits_filename': "./forced_split_master.json"}
            self.model = RandomizedSearchCV(
                estimator=LGBMClassifier(**model_params),
                param_distributions={
                    'class_weight': [{1:x, 0:1} for x in [1, 2, 4, 8, 16]],
                    'n_estimators': poisson(150),
                    'max_depth': poisson(5)
                },
                cv=5,
                #scoring=make_scorer(fbeta_score, beta=1000),
                scoring='recall',
                n_iter = 30
                )
            #self.model = LGBMClassifier(**model_params)
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
        print("Training model. Please wait.")
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
        n_valid_data = len(yp)

        recall = recall_score(yv,yp)
        precision = precision_score(yv,yp)
        accuracy = accuracy_score(yv,yp)

        yp_prob = [p[1] for p in self.predict_probabilities(xv,predictors)]
        roc_auc = roc_auc_score(yv,yp_prob)

        return {
            "n_valid_data": n_valid_data,
            "recall": recall,
            "precision": precision,
            "accuracy": accuracy,
            "roc_auc": roc_auc
            }