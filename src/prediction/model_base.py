import functools
import pickle

class BasePredictionModel():

    def __init__(self,model_pickle=None):
        if model_pickle:
            self.is_trained = True
            self.model = pickle.loads(model_pickle)
        else:
            self.is_trained = False
            self.model = None

    # Decorator to check if model exists.
    def check_model_exists(func):
        @functools.wraps(func)
        def wrapper(self,*args,**kwargs):
            if self.model is None:
                raise Exception("ERROR: No model specified.")
            value = func(self,*args,**kwargs)
            return value
        return wrapper

    # Decorator to check if model has been trained.
    def check_model_trained(func):
        @functools.wraps(func)
        def wrapper(self,*args,**kwargs):
            if not self.is_trained:
                raise Exception("ERROR: Model not trained yet.")
            value = func(self,*args,**kwargs)
            return value
        return wrapper

    # Train the model, if it exists.
    @check_model_exists
    def train(self):
        pass

    # Predict using the model, if it exists and has been trained.
    @check_model_exists
    @check_model_trained
    def predict(self):
        pass

    # Validate the model, if it exists and has been trained.
    @check_model_exists
    @check_model_trained
    def validate(self):
        pass

    # Get the pickle representation of the model, if it exists and has been trained.
    @check_model_exists
    @check_model_trained
    def as_pickle(self):
        return pickle.dumps(self.model)

    # Save the model as a pickle, if it exists and has been trained.
    @check_model_exists
    @check_model_trained
    def save_as_pickle(self,filename):
        pickle.dump(self.model,open(filename,'wb'))
