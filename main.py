import os

from azure.storage.blob import BlobClient
from flask import Flask, jsonify, request
from azure.storage.blob import BlobClient

import prediction as pd
import db
import utils


app = Flask(__name__)


container_name = os.getenv("CONTAINER_NAME")
connection_string = os.getenv("CONNECTION_STRING")



@app.route('/predict/', methods=['POST'])
async def predict():
    image = request.files.get('image')
    image_id = request.form.get('image_id')
    name = request.form.get('name')
    age = request.form.get('age')

    normalized_image = pd.normalize_image(image)
    prediction_result = pd.make_prediction(normalized_image)
    classification_result = pd.classify(prediction_result)
    


    try:
        db.insert(name, age, prediction_result, classification_result, image_id)
        return jsonify({'prediction_result': str(prediction_result[0][0]), 'classification_result': classification_result})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/upload/', methods=['POST'])
def upload_blob():
    image = request.files.get('image')
    name = request.form.get('name')
    image_id = utils.format_file_name(name)
    blob_client = BlobClient.from_connection_string(conn_str=connection_string, container_name=container_name, blob_name=image_id)
    blob_client.upload_blob(image)

    return jsonify({'image_id': image_id})


@app.route('model_version', methods=['GET'])
def get_model_version():
    return jsonify({'model_version': '1.0.0'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
