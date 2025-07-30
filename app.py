from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Load your model
model = load_model("best_waste_classifier.h5")

# Image size used during training
IMG_SIZE = (224, 224)

# Class labels
class_names = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']

# Home route to render the webcam page
@app.route('/')
def index():
    return render_template('index.html')

# Prediction route (used by HTML)
@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    filename = secure_filename(file.filename)
    filepath = os.path.join("uploads", filename)
    os.makedirs("uploads", exist_ok=True)
    file.save(filepath)

    # Load and preprocess image
    img = image.load_img(filepath, target_size=IMG_SIZE)
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Predict
    predictions = model.predict(img_array)
    predicted_index = np.argmax(predictions)
    predicted_class = class_names[predicted_index]
    confidence = float(np.max(predictions))

    # Determine bin type
    bin_type = "Recyclable"
    if predicted_class in ['Biodegradable', 'Organic']:
        bin_type = "Compost"
    elif predicted_class in ['Battery', 'E-waste']:
        bin_type = "Hazardous"

    return jsonify({
        'filename': filename,
        'predicted_class': predicted_class,
        'confidence': round(confidence, 2),
        'suggested_bin': bin_type
    })

if __name__ == '__main__':
    app.run(debug=True)
