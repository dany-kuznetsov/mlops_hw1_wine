# Imports
from flask import Flask
from flask_restx import Api, Resource

import pandas as pd
import json
import joblib
from pathlib import Path

from werkzeug.datastructures import FileStorage
import os

import models_module

# Models and features available
model_types_list = ['Ridge', 'DecisionTreeClassifier']
feature_cols = [
    'fixed acidity', 'volatile acidity', 'citric acid', 'residual sugar',
    'chlorides', 'free sulfur dioxide', 'total sulfur dioxide', 'density',
    'pH', 'sulphates', 'alcohol']
y_col = 'quality'

# Directory for models
model_dir = Path('../models')
model_dir.mkdir(exist_ok=True)

app = Flask(__name__)
api = Api(app)

# Fields parser for fit section
upload_parser_fit = api.parser()
upload_parser_fit.add_argument('file', location='files', type=FileStorage, required=True)
upload_parser_fit.add_argument('model_id', required=True, location='args')
upload_parser_fit.add_argument('model_type', required=True, location='args', choices=model_types_list)
upload_parser_fit.add_argument('model_params', required=False, location='args')

# Fields parser for prediction section
upload_parser_predict = api.parser()
upload_parser_predict.add_argument('file', location='files', type=FileStorage, required=True)
upload_parser_predict.add_argument('model_id', required=True, location='args')

# Fields parser for delete section
params_to_delete_model = api.parser()
params_to_delete_model.add_argument('model_id', required=True, location='args')


def read_file(file):
    """Read the data uploaded by user"""
    try:
        data = pd.read_excel(file)
    except Exception as e:
        raise ValueError(f"Couldn't read file: {e}")
    return data


@api.route('/fit', methods=['PUT'],
           doc={'description': 'Fit model on uploaded data'})
@api.expect(upload_parser_fit)
class Fit(Resource):
    @api.doc(params={
        'file': f'Upload excel file with columns: {feature_cols + [y_col]}',
        'model_id': 'Model Identification Code',
        'model_type': 'model type like Ridge or DecisionTreeClassifier',
        'model_params': 'json with hyperparameters to train model', })
    @api.response(200, 'Success')
    @api.response(400, 'Validation Error')
    def put(self):
        args = upload_parser_fit.parse_args()
        model_id = args['model_id']
        model_type = args['model_type']
        model_params = args['model_params']
        if model_params is not None:
            model_params = json.loads(model_params)
        try:
            data = read_file(args['file'])
        except ValueError as e:
            return str(e), 400

        model = models_module.MyModel(model_id, model_type)
        model.fit(data, model_params)

        joblib.dump(model, model_dir / f'{model_id}.pkl')
        return 'Model is fitted to uploaded data', 200


@api.route('/predict', methods=['POST'],
           doc={'description': 'Make prediction on uploaded data'})
@api.expect(upload_parser_predict)
class Predict(Resource):
    @api.doc(params={
        'file': f'Upload excel file with columns: {feature_cols + [y_col]}',
        'model_id': 'Model Identification Code',
    })
    @api.response(200, 'Success')
    @api.response(400, 'Validation Error')
    def post(self):
        args = upload_parser_predict.parse_args()
        model_id = args['model_id']
        model_path_to_file = model_dir / f'{model_id}.pkl'
        if not model_path_to_file.exists():
            return "Model does not exist", 400
        model = joblib.load(model_path_to_file)

        try:
            data = read_file(args['file'])
        except ValueError as e:
            return str(e), 400

        pred = model.predict(data)

        return {'pred': pred.tolist()}

@api.route('/delete_model')
class DeleteModel(Resource):
    @api.expect(params_to_delete_model)
    @api.response(200, 'Success')
    @api.response(400, 'Bad Request')
    def delete(self):
        args = params_to_delete_model.parse_args()
        model_id = args['model_id']
        model_path_to_file = model_dir / f'{model_id}.pkl'
        if os.path.exists(model_path_to_file):
            os.remove(model_path_to_file)
            return f"model is deleted successfully", 200
        else:
            return f"model {model_id} does not exist", 400


@api.route('/saved_models_list')
class SavedModelsList(Resource):
    @api.response(200, 'Success')
    @api.response(500, 'Internal Server Error')
    def get(self):
        if os.path.exists('../models'):
            return [x for x in os.listdir('../models/') if '.pkl' in x]
        else:
            return 500, 'models directory does not exist'


@api.route('/model_types_available')
class ModelTypesAvailable(Resource):
    @api.response(200, 'Success')
    @api.response(500, 'Internal Server Error')
    def get(self):
        return model_types_list


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
