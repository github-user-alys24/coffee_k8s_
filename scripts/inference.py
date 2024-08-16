# Allows user to input values and return the predicted revenue
from flask import Flask, send_file, request, jsonify
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

# Get paths
models = ['gbt_model.pkl']
gbt_model_path = os.path.join(model_dir, models[0])

# Load
gbt = joblib.load(gbt_model_path)

def pred():
    # Get data from the request
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form 
    # Extract month from data
    month = data.get('month')
    month = int(month)
    # Validate the input
    if month is None:
        return jsonify({"error": "Month is required"}), 400
    
    # Prepare the data for prediction
    hours = list(range(6, 21))
    month = month+ 6
    # Make predictions with GBT
    input_pred = pd.DataFrame({"Month": [month]* len(hours), 'Hour': hours})
    y_pred= gbt.predict(input_pred)
    input_pred['predictedRevenue'] = y_pred
    # Calculate the total predicted revenue
    total_predicted_revenue = round(input_pred['predictedRevenue'].sum(), 2)

    input_pred_json = input_pred.to_dict(orient='records')
    xy_data = {
        'Table': input_pred_json,
        'Predicted Overall Revenue ($)': total_predicted_revenue
    }
    return jsonify(xy_data)

class Predict(Resource):
    def post(self):
        return pred()
    def get(self):
        return pred()
        
# Add resources to the API
api.add_resource(Predict, '/predict')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
