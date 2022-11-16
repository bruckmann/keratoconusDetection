import os

from azure.storage.blob import BlobClient
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from azure.storage.blob import BlobClient

import prediction as pd
import db
import utils


app = Flask(__name__)
CORS(app)


container_name = os.getenv("CONTAINER_NAME")
connection_string = os.getenv("CONNECTION_STRING")



@app.route('/predict/', methods=['POST'])
async def predict():
    image_to_normalize = request.files.get('image')
    image_to_blob = request.files.get('image')
    name = request.form.get('name')
    age = request.form.get('age')

    normalized_image = pd.normalize_image(image_to_normalize)
    prediction_result = pd.make_prediction(normalized_image)
    classification_result = pd.classify(prediction_result)
    file_name = utils.format_file_name(name)
    


    try:
        db.insert(name, age, prediction_result, classification_result, file_name)
        blob = BlobClient.from_connection_string(conn_str=connection_string, container_name=container_name, blob_name=file_name, logging_enable=True)
        blob.upload_blob(data=image_to_blob)
        return jsonify({'prediction_result': str(prediction_result[0][0]), 'classification_result': classification_result})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/upload/', methods=['GET'])
def predict_version():
    return "1.0.0"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
