import uuid
import os
from io import BytesIO

import numpy as np
import tensorflow as tf
from azure.storage.blob import BlobClient
from flask import Flask, request, jsonify

import prediction as pd

app = Flask(__name__)


@app.route('/predict/', methods=['POST'])
async def predict():
    image = request.files.get('image')
    name = request.form.get('name')
    age = request.form.get('age')

    file_name_on_blob = insert_on_blob(name, image)
    prediction_result = pd.make_prediction(pd.normalize_image(image))
    return jsonify({'prediction_result': str(prediction_result[0][0]), 'nameOnBlob': file_name_on_blob})

@app.route('/upload/', methods=['GET'])
def predict_version():
    return "1.0.0"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
