from scripts import models_module
import pandas as pd


def test_model_maker_ridge_empty_params():
    data = pd.read_excel('data/winequality-white_train.xlsx')
    model = models_module.MyModel(model_id=-1, model_type='Ridge')
    model.fit(data, model_params={})
    prediction = model.predict(data)
    print(prediction)
    assert len(data) == len(prediction)
    assert min(prediction) > 0
    assert max(prediction) < 100


def test_model_maker_ridge_with_params():
    data = pd.read_excel('data/winequality-white_train.xlsx')
    model = models_module.MyModel(model_id=-1, model_type='Ridge')
    model.fit(data, model_params={'alpha': 10})
    prediction = model.predict(data)
    print(prediction)
    assert len(data) == len(prediction)
    assert min(prediction) > 0
    assert max(prediction) < 100


def test_model_maker_tree_with_params():
    data = pd.read_excel('data/winequality-white_train.xlsx')
    model = models_module.MyModel(model_id=-1, model_type='DecisionTreeClassifier')
    model.fit(data, model_params={'max_depth': 3})
    prediction = model.predict(data)
    print(prediction)
    assert len(data) == len(prediction)
    assert min(prediction) > 0
    assert max(prediction) < 100
