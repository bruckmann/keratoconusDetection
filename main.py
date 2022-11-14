import uuid
import os
from io import BytesIO

import numpy as np
import tensorflow as tf
from azure.storage.blob import BlobClient
from flask import Flask, request, jsonify

import model

app = Flask(__name__)

container_name = os.getenv("CONTAINER_NAME")
connection_string = os.getenv("CONNECTION_STRING")

def format_file_name(person_name: str):
    return person_name.replace(" ", "-") + "-" + str(uuid.uuid4())

def insert_on_blob(person_name: str, image):
    name_to_save = format_file_name(person_name)
    blob = BlobClient.from_connection_string(conn_str=connection_string, container_name=container_name, blob_name=name_to_save)
    blob.upload_blob(data=image)
    return name_to_save

@app.route('/predict/', methods=['POST'])
async def predict():
    image = request.files.get('image')
    name = request.form.get('name')
    age = request.form.get('age')
    prediction_result = model.make_prediction(model.normalize_image(image))
    return jsonify({'prediction_result': prediction_result})

@app.route('/upload/', methods=['GET'])
def predict_version():
    return "1.0.0"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
