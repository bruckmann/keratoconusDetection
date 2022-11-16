import os

from azure.storage.blob import BlobClient
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from azure.storage.blob import BlobClient

import prediction as pd
import db
import blob


app = Flask(__name__)
CORS(app)


container_name = os.getenv("CONTAINER_NAME")
connection_string = os.getenv("CONNECTION_STRING")


@app.route('/predict/', methods=['POST'])
async def predict():
    image_to_normalize = request.files.get('image')
    image_to_blob = request.form.get('image')
    name = request.form.get('name')
    age = request.form.get('age')

    normalized_image = pd.normalize_image(image_to_normalize)
    prediction_result = pd.make_prediction(normalized_image)
    classification_result = pd.classify(prediction_result)

    try:
        file_name_on_blob = blob.insert_on_blob(name, image_to_blob)  
        db.insert(name, age, prediction_result, classification_result, file_name_on_blob)
        return jsonify({'prediction_result': str(prediction_result[0][0]), 'classification_result': classification_result})
    except Exception as e:
        print(e)

@app.route('/upload/', methods=['GET'])
def predict_version():
    return "1.0.0"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
