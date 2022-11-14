import os

from azure.storage.blob import BlobClient
from flask import Flask, jsonify, request
from azure.storage.blob import BlobClient

import prediction as pd
import utils

app = Flask(__name__)


container_name = os.getenv("CONTAINER_NAME")
connection_string = os.getenv("CONNECTION_STRING")


@app.route('/predict/', methods=['POST'])
async def predict():
    image = request.files.get('image')
    name = request.form.get('name')
    age = request.form.get('age')

    normalized_image = pd.normalize_image(image)
    prediction_result = pd.make_prediction(normalized_image)
  
    file_name_on_blob = utils.format_file_name(name)
    blob = BlobClient.from_connection_string(conn_str=connection_string, container_name=container_name, blob_name=file_name_on_blob)
    blob.upload_blob(data=image)
    return jsonify({'prediction_result': str(prediction_result[0][0]), 'file_name_on_blob': file_name_on_blob})

@app.route('/upload/', methods=['GET'])
def predict_version():
    return "1.0.0"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
