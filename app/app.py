from flask import Flask, request, jsonify, send_from_directory
import tensorflow as tf
from tensorflow.keras.models import load_model, Model
from tensorflow.keras.layers import Input, TFSMLayer
from PIL import Image
import numpy as np
import sys
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)

# Load model
try:
    model_path = "/Users/kenlam/Desktop/Data science/ML projects/mold_detector2/app/saved_model(kaggle)"
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model path '{model_path}' does not exist.")
    
    input_tensor = Input(shape=(299, 299, 3))
    tfsm_layer = TFSMLayer(model_path, call_endpoint="serving_default")(input_tensor)
    model = Model(inputs=input_tensor, outputs=tfsm_layer)
    print("Model loaded successfully.")
    sys.stdout.flush()
except Exception as e:
    print(f"Error loading model: {e}")
    sys.exit(1)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Set the folder to store uploaded images
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload/', methods=['POST'])
def upload_image():
    if 'image' not in request.files: # if not detect an image
        return jsonify({'error': 'No image uploaded!'}), 400
    
    # If uploaded an image
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

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
        print(f"Processed image! Shape: {image_array.shape}")
        sys.stdout.flush()
        print("Model predicting...")
        prediction_dict = model.predict(image_array)
        print(f"Raw prediction output: {prediction_dict}")
        sys.stdout.flush()

        if 'output_0' not in prediction_dict:
            raise ValueError("Prediction dictionary does not contain 'output_0' key.")
        
        prediction_array = prediction_dict['output_0']
        prediction_value = prediction_array[0][0]
        print(f"Prediction value: {prediction_value}")
        sys.stdout.flush()

        classification = "Moldy!" if prediction_value > 0.5 else "Not moldy!"

        return jsonify({'classification': classification})
    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
     # Ensure the upload folder exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)