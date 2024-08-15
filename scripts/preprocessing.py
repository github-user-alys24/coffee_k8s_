from flask import Flask, send_file
from flask_restful import Resource, Api
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from io import BytesIO
from sklearn.model_selection import train_test_split

# Instantiate the app
app = Flask(__name__)
api = Api(app)

# Define the path to the data directory
data_dir = '/raw_data'
output_dir = '/preprocessed_data'

# Load the data
data_file = os.path.join(data_dir, 'coffee_shop.csv')

# Check if the file exists
if not os.path.isfile(data_file):
    raise FileNotFoundError(f"The data file {data_file} does not exist.")

data = pd.read_csv(data_file)

required_columns = [
    'transaction_qty', 'store_id', 'product_id', 'unit_price',
    'product_category', 'product_type', 'Revenue', 'Month', 'Weekday', 'Hour'
]

data_filtered = data[required_columns]
data_month_hour = data_filtered.groupby(['Month', 'Hour']).agg({'Revenue': 'sum'}).reset_index()

X = data_month_hour[['Month','Hour']]
y = data_month_hour['Revenue']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

result = data_month_hour.to_dict(orient='records')
result_file = os.path.join(output_dir, 'result.json')

# Save JSON and CSV files
pd.DataFrame(result).to_json(result_file, orient='records')
X_train.to_csv(f'{output_dir}/X_train.csv', index=False)
X_test.to_csv(f'{output_dir}/X_test.csv', index=False)
y_train.to_csv(f'{output_dir}/y_train.csv', index=False, header=False)
y_test.to_csv(f'{output_dir}/y_test.csv', index=False, header=False)

class prodType(Resource):
    def get(self):
        agged = data.groupby('product_type').agg({'transaction_qty': 'sum', 'Revenue': 'sum'}).sort_values(by='Revenue', ascending=True).reset_index()
        ress = agged.to_dict(orient='records')
        return ress

class Dataframe(Resource):
    def get(self):
        res = data_month_hour.to_dict(orient='records')
        return res

class top25rows(Resource):
    def get(self):
        top25rows = data.head(25)
        ress = top25rows.to_dict(orient='records')
        return ress
        
class Products(Resource):
    def get(self):
        agged = data.groupby('product_category').agg({'transaction_qty': 'sum', 'Revenue': 'sum'}).sort_values(by='Revenue', ascending=True).reset_index()
        ress = agged.to_dict(orient='records')
        return ress

class baseGraph(Resource):
    def get(self):
        fig, ax = plt.subplots(1, 2, figsize=(16, 7))
        agged = data.groupby('store_location').agg({'Revenue': 'sum'}).reset_index()

        sns.barplot(x='store_location', y='Revenue', data=agged.sort_values(by='Revenue', ascending=True), 
                    ax=ax[0], palette="pastel")
        ax[0].grid(True)
        ax[0].set_title("Total Revenue by Store Location")

        agged_month = data.groupby('product_type').agg({'Revenue': 'sum'}).reset_index()
        sns.barplot(x='product_type', y='Revenue', data=agged_month, ax=ax[1], palette="pastel")
        ax[1].set_title("product_type by Revenue")

        # Adjust layout
        plt.tight_layout()
        plt.show()
        
        img1 = BytesIO()
        plt.savefig(img1, format='png')
        img1.seek(0)
        return send_file(img1, mimetype='image/png')

class PlotGraph(Resource):
    def get(self):
        # Add debug print statements to verify code execution
        print("PlotGraph endpoint reached")

        required_columns = [
            'transaction_qty', 'store_id', 'product_id', 'unit_price',
            'product_category', 'product_type', 'Revenue', 'Month', 'Weekday', 'Hour'
        ]
        
        for col in required_columns:
            if col not in data.columns:
                return {"error": f"Column {col} is missing from the data."}, 400

        data_filtered = data[required_columns]
        data_month_hour = data_filtered.groupby(['Month', 'Hour']).agg({'Revenue': 'sum'}).reset_index()

        fig, ax = plt.subplots(1, 2, figsize=(12, 5))
        agg = data_month_hour.groupby(['Month',
                                 ]).agg({'Revenue': 'sum',
                                        }).reset_index()
        agg_sorted = agg.sort_values(by='Revenue', ascending=False)
        sns.lineplot(ax=ax[0],data=agg_sorted, x='Month', y='Revenue',
                     color='#587a68', markers=True).grid(True)
        sns.scatterplot(ax=ax[0],data=agg_sorted, x='Month', y='Revenue',
                        color='#587a68', legend=False)
        palette = sns.color_palette("Set2")
        sns.lineplot(ax=ax[1],data=data_month_hour, x='Hour', y='Revenue', legend=False)
        sns.scatterplot(ax=ax[1],data=data_month_hour, x='Hour', y='Revenue', legend=False)
        ax[0].set_title("Total Revenue earned each Month")
        ax[1].set_title("Revenue by Hour")
        plt.show()

        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)

        return send_file(img, mimetype='image/png')

api.add_resource(Dataframe, '/')
api.add_resource(top25rows, '/top25rows')
api.add_resource(PlotGraph, '/graph')
api.add_resource(baseGraph, '/1graph')
api.add_resource(Products, '/products')
api.add_resource(prodType, '/product_type')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
