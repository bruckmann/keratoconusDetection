import os

from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

import prediction as pd
import db

app = Flask(__name__)
CORS(app)

@app.route('/predict/', methods=['POST'])
async def predict():
    image_to_normalize = request.files.get('image')
    image_id = request.form.get('image_id')
    name = request.form.get('name')
    age = request.form.get('age')

    normalized_image = pd.normalize_image(image_to_normalize)
    prediction_result = pd.make_prediction(normalized_image)
    classification_result = pd.classify(prediction_result)
    
    try:
        db.insert(name, age, prediction_result, classification_result, image_id)
        return jsonify({'prediction_result': str(prediction_result[0][0]), 'classification_result': classification_result})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/upload/', methods=['GET'])
def predict_version():
    return "1.0.0"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
