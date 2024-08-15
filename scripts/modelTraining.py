from flask import Flask, send_file
from flask_restful import Resource, Api

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

import os
from io import BytesIO
import joblib

from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor

# Instantiate the app
app = Flask(__name__)
api = Api(app)

# Define the path to the data directory
input_dir = '/preprocessed_data'
output_dir = '/model'

# Read files from input_dir
X_train = pd.read_csv(f'{input_dir}/X_train.csv')
X_test = pd.read_csv(f'{input_dir}/X_test.csv')
y_train = pd.read_csv(f'{input_dir}/y_train.csv', header=None)
y_test = pd.read_csv(f'{input_dir}/y_test.csv', header=None)
y_train, y_test = np.ravel(y_train), np.ravel(y_test)

# GBT
gbt = GradientBoostingRegressor(n_estimators=100, max_depth=3, random_state=42)
gbt.fit(X_train, y_train)
y_pred = gbt.predict(X_test)


def evaluation_metrics(y_test, y_pred, model):
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    print(f"Metrics for {model}")
    print("Root Mean Squared Error (RMSE):", rmse)
    print("Mean Absolute Error (MAE):", mae)
    print("R-squared:", r2)
    return rmse,r2,mae

class XyShape(Resource):
    def get(self):
        xy_data = {
            'X and y data': ['X_train', 'X_test', 'y_train', 'y_test'],
            'Shape': [X_train.shape, X_test.shape, y_train.shape, y_test.shape]
        }
        # Create a DataFrame from the dictionary
        xy_df = pd.DataFrame(xy_data)
        res = xy_df.to_dict(orient='records')
        return res

class modelTraining_gbt(Resource):
    def get(self):
        joblib.dump(gbt, f'{output_dir}/gbt_model.pkl')
        return {"message": "success"}, 200

class Metrics(Resource):
    def get(self):
        gbt.fit(X_train, y_train)
        y_pred = gbt.predict(X_test)
        baseRMSE, baseR2, baseMAE = evaluation_metrics(y_test, y_pred, "base GBT model")
        metrics_data_gbt = {
            'Metric': ['Root Mean Squared Error (RMSE)', 'Mean Absolute Error (MAE)', 'R-squared (R2)'],
            'Value': [baseRMSE, baseMAE, baseR2]
        }
        # Create a DataFrame from the dictionary
        metrics_gbt = pd.DataFrame(metrics_data_gbt)
        res = metrics_gbt.to_dict(orient='records')
        return res
        
class featureImportances_gbt(Resource):
    def get(self):
        feature_cols= ['Month', 'Hour']
        feature_imp = pd.Series(gbt.feature_importances_, index=feature_cols).sort_values(ascending=False)
        fig = plt.figure(figsize=(12,5))
        ax = feature_imp.plot(kind='bar',color='maroon')
        ax.set(title='GBT Relative Importance Bar Chart')
        ax.set(xlabel='Attributes to revenue')
        ax.set(ylabel='Relative Importance')
        for i, value in enumerate(feature_imp):
            ax.text(i, value + 0.02, f'{value:.2f}', ha='center', va='bottom')
        ax.set_ylim(0, max(feature_imp) + 0.1) 
        ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
        plt.show()
        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        return send_file(img, mimetype='image/png')

api.add_resource(modelTraining_gbt, '/gbt')
api.add_resource(XyShape, '/shape')
api.add_resource(featureImportances_gbt, '/importances_gbt')
api.add_resource(Metrics, '/')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
