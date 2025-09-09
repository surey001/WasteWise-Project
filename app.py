from flask import Flask, request, jsonify, render_template
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
import numpy as np
import pyttsx3
from langdetect import detect
import threading

app = Flask(__name__)

# Load your trained model
model = load_model("best_waste_classifier.h5")
class_labels = ['Cardboard', 'Glass', 'Metal', 'Paper', 'Plastic', 'Trash']

# Bin suggestions
bin_suggestions = {
    'Cardboard': 'Blue',
    'Glass': 'Blue',
    'Metal': 'Blue',
    'Paper': 'Blue',
    'Plastic': 'Yellow',
    'Trash': 'Black'  # Add fallback
}

# Disposal tips
disposal_tips_en = {
    'Glass': 'Do not mix broken glass with regular trash.',
    'Metal': 'Rinse and reuse metal containers before disposal.',
    'Paper': 'Avoid wetting paper waste for better recycling.',
    'Plastic': 'Separate clean plastic for recycling.',
    'Cardboard': 'Flatten boxes before disposal.',
    'Trash': 'Dispose of non-recyclables responsibly.'
}

disposal_tips_ta = {
    'Glass': 'உடைந்த கண்ணாடியை வெவ்வேறு மூட்டையில் போடுங்கள்.',
    'Metal': 'மெட்டல் பொருட்களை சுத்தம் செய்து மீண்டும் பயன்படுத்துங்கள்.',
    'Paper': 'காகிதத்தை ஈரமாகச் செய்யாமல் பிரித்து சேகரிக்கவும்.',
    'Plastic': 'தூய பிளாஸ்டிக்குகளை தனியாக சேகரிக்கவும்.',
    'Cardboard': 'கார்ட்போர்டு பெட்டிகளை தட்டையாக மடிக்கவும்.',
    'Trash': 'மறுசுழற்சி செய்ய முடியாதவற்றை பொறுப்புடன் முகாமையிடுங்கள்.'
}

# Speak function in a thread
def speak_text(text, lang='en'):
    def run():
        engine = pyttsx3.init()
        engine.setProperty('rate', 160)
        engine.setProperty('volume', 1.0)

        voices = engine.getProperty('voices')
        selected_voice = None

        if lang == "ta":
            for voice in voices:
                if 'tamil' in voice.name.lower() or 'ta' in voice.id.lower():
                    selected_voice = voice.id
                    break
        elif lang == "en":
            for voice in voices:
                if 'english' in voice.name.lower() and 'india' in voice.id.lower():
                    selected_voice = voice.id
                    break

        engine.setProperty('voice', selected_voice or voices[0].id)
        engine.say(text)
        engine.runAndWait()
        engine.stop()

    threading.Thread(target=run).start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']
    img = Image.open(image_file).convert("RGB")
    img = img.resize((224, 224))
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)
    predicted_class_index = np.argmax(prediction)
    predicted_class = class_labels[predicted_class_index]
    confidence = f"{(prediction[0][predicted_class_index] * 100):.2f}%"
    suggested_bin = bin_suggestions.get(predicted_class, "Black")

    # Detect language
    lang = "en"
    try:
        if detect(disposal_tips_ta[predicted_class]) == "ta":
            lang = "ta"
    except:
        lang = "en"

    disposal_tip = disposal_tips_ta.get(predicted_class) if lang == "ta" else disposal_tips_en.get(predicted_class, "")

    # Construct and speak message
    message = f"{predicted_class}. Use {suggested_bin} bin."
    if disposal_tip:
        message += f" Tip: {disposal_tip}"

    speak_text(message, lang)

    return jsonify({
        "predicted_class": predicted_class,
        "confidence": confidence,
        "suggested_bin": suggested_bin,
        "disposal_tip": disposal_tip,
        "language": lang
    })

if __name__ == "__main__":
    app.run(debug=True)
