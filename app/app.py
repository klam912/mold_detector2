from flask import Flask, request, jsonify
import tensorflow as tf
from tensorflow.keras.models import load_model, Model
from tensorflow.keras.layers import Input, TFSMLayer
from PIL import Image
import numpy as np
import sys


app = Flask(__name__)

# Load model
# model = load_model('/Users/kenlam/Desktop/Data science/ML projects/project7.1/mold_detector1/model/model.h5')
input_tensor = Input(shape=(299, 299, 3))
tfsm_layer = TFSMLayer("saved_model", call_endpoint="serving_default")(input_tensor)
model = Model(inputs=input_tensor, outputs=tfsm_layer)

@app.route('/')
def index():
    return "Welcome to the Mold Detector API. Use the /upload endpoint to upload an image for classification."


@app.route('/upload/', methods=['POST'])
def upload_image():
    if request.method != 'POST':
        return jsonify({'error': 'Invalid request method'}), 405
    
    if 'image' not in request.files: # if not detect an image
        return jsonify({'error': 'No image uploaded!'}), 400
    
    # If uploaded an image
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    print("File ready to be predicted!")
    sys.stdout.flush()
    try:
        print("Opening the image")
        sys.stdout.flush()
        image = Image.open(file).resize((299,299)) # resize image to fit our model's input
        print("Finished opening the image")
        sys.stdout.flush()
        image_array = np.array(image) / 255.0
        image_array = np.expand_dims(image_array, axis=0)
        print(f"Processed image!")
        sys.stdout.flush()
        # print("Model summary")
        # model.summary()
        print("Model predicting...")
        prediction = model.predict(image_array)
        print(prediction[0])
        sys.stdout.flush()
        classification = "Moldy!" if prediction[0] > 0.5 else "Not moldy!"

        return jsonify({'classification': classification})
    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug=True)