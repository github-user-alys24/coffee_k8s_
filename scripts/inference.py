from flask import Flask, send_file
from flask_restful import Resource, Api

import pandas as pd
import numpy as np

from sklearn.ensemble import GradientBoostingRegressor

import os
import joblib

from io import BytesIO

# Instantiate the app
app = Flask(__name__)
api = Api(app)

# Define the path to the data directory
model_dir = '/model'
input_dir = '/preprocessed_data'

# Get paths
models = ['gbt_model.pkl']
gbt_model_path = os.path.join(model_dir, models[0])

# Load
gbt = joblib.load(gbt_model_path)

# Read files from input_dir
X_test = pd.read_csv(f'{input_dir}/X_test.csv')
y_train = pd.read_csv(f'{input_dir}/y_train.csv', header=None)
y_test = pd.read_csv(f'{input_dir}/y_test.csv', header=None)
y_train, y_test = np.ravel(y_train), np.ravel(y_test)

# GBT prediction
y_pred_gbt = gbt.predict(X_test)

class inference_gbt(Resource):
    def get(self):
        y_pred = gbt.predict(X_test)
        results = pd.DataFrame({
            'Actual': y_test, 
            'Predicted': y_pred_gbt,
            'Difference %': 100 - (y_test/y_pred_gbt)*100
        })
        print(results.head(25))
        result = results.head(25).to_dict(orient='records')
        return result

api.add_resource(inference_gbt, '/')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
