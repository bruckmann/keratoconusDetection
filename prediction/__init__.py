import tensorflow as tf
import numpy as np

from io import BytesIO

def normalize_image(image):
    normalized_image = tf.keras.utils.load_img(BytesIO(image.read()), target_size = (224, 224))
    normalized_image = tf.keras.utils.img_to_array(normalized_image)
    normalized_image = np.expand_dims(normalized_image, axis = 0)
    return normalized_image

async def make_prediction(normalized_image):
    model = tf.keras.models.load_model("./prediction/model/EyeScan.h5")
    prediction = await model.predict(normalized_image)
    return prediction