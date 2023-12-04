import numpy as np
from sklearn.ensemble import IsolationForest
from flask import Flask, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

app = Flask(__name__)
training_data = pd.read_csv('training_data.csv')
input_data = training_data['query'].values
output_data = training_data['label'].values
label_encoder = LabelEncoder()
encoded_input_data = label_encoder.fit_transform(input_data)
model = RandomForestRegressor(n_estimators=100)  
model.fit(encoded_input_data.reshape(-1, 1), output_data)
@app.route('/process', methods=['POST'])
def process_request():
    try:
        data = request.json
        if 'input' in data:
            sql_query = [data['input']]
        print (sql_query)
        X_test_encoded = label_encoder.transform(sql_query)
        prediction = model.predict(X_test_encoded.reshape(-1, 1))
        y_pred_rounded = [int(round(val)) for val in prediction]
        if prediction[0] < 0:
            return jsonify({"message": "Potential SQL injection detected."})
        else:
            return jsonify({"message": "Query executed successfully."})
    except Exception as e:
        print(e)
        return jsonify({"message": "Error processing the request."})
if __name__ == '__main__':
    app.run(debug=True)
