import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.tree import DecisionTreeClassifier


class MyModel:
    """
    My model - create, fit, predict

    Args:
        model_id (int): model identification code
        model_type (str): choose model class 'Ridge' or 'DecisionTreeClassifier'
    """

    def __init__(self, model_id, model_type):
        self.feature_cols = [
            'fixed acidity', 'volatile acidity', 'citric acid', 'residual sugar',
            'chlorides', 'free sulfur dioxide', 'total sulfur dioxide', 'density',
            'pH', 'sulphates', 'alcohol']
        self.y_col = 'quality'
        models_dict = {'Ridge': Ridge(), 'DecisionTreeClassifier': DecisionTreeClassifier()}
        self.model_id = model_id
        self.model_type = model_type
        self.model = models_dict[model_type]

    def fit(self, data, model_params):
        '''Fit to the data with chosen hyperparameters'''
        if model_params is not None:
            self.model.set_params(**model_params)
        self.model.fit(X=data[self.feature_cols], y=data[self.y_col])

    def predict(self, data):
        y_pred = self.model.predict(data[self.feature_cols])
        return y_pred
