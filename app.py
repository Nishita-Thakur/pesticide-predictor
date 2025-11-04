from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os

app = Flask(__name__)
CORS(app)

# Load your model
model = load_model("plant_disease_model_fixed.keras")

# Class names (make sure this matches your model output)
class_names = [
    'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
    'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_',
    'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot',
    'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy',
    'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight',
    'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy',
    'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot',
    'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot',
    'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus', 'Tomato___healthy'
]

# Complete pesticide suggestions dictionary (fill or edit as you want)
pesticide_dict = {
    'Apple___Apple_scab': 'Use sulfur-based fungicides such as sulfur or captan.',
    'Apple___Black_rot': 'Apply fungicides like Captan or Mancozeb.',
    'Apple___Cedar_apple_rust': 'Use myclobutanil or other fungicides recommended for rust.',
    'Apple___healthy': 'No pesticide needed, plant is healthy.',
    'Blueberry___healthy': 'No pesticide needed, plant is healthy.',
    'Cherry_(including_sour)___Powdery_mildew': 'Apply sulfur or neem oil sprays.',
    'Cherry_(including_sour)___healthy': 'No pesticide needed, plant is healthy.',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot': 'Use fungicides containing azoxystrobin.',
    'Corn_(maize)___Common_rust_': 'Apply fungicides such as propiconazole or azoxystrobin.',
    'Corn_(maize)___Northern_Leaf_Blight': 'Use fungicides like chlorothalonil or mancozeb.',
    'Corn_(maize)___healthy': 'No pesticide needed, plant is healthy.',
    'Grape___Black_rot': 'Apply fungicides such as sulfur or captan.',
    'Grape___Esca_(Black_Measles)': 'Use fungicides and pruning to remove infected wood.',
    'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)': 'Apply copper-based fungicides.',
    'Grape___healthy': 'No pesticide needed, plant is healthy.',
    'Orange___Haunglongbing_(Citrus_greening)': 'Remove infected trees and control psyllid vector.',
    'Peach___Bacterial_spot': 'Use copper-based bactericides regularly.',
    'Peach___healthy': 'No pesticide needed, plant is healthy.',
    'Pepper,_bell___Bacterial_spot': 'Apply copper-based bactericides.',
    'Pepper,_bell___healthy': 'No pesticide needed, plant is healthy.',
    'Potato___Early_blight': 'Use fungicides like chlorothalonil or mancozeb.',
    'Potato___Late_blight': 'Apply fungicides such as metalaxyl or chlorothalonil.',
    'Potato___healthy': 'No pesticide needed, plant is healthy.',
    'Raspberry___healthy': 'No pesticide needed, plant is healthy.',
    'Soybean___healthy': 'No pesticide needed, plant is healthy.',
    'Squash___Powdery_mildew': 'Use sulfur or potassium bicarbonate sprays.',
    'Strawberry___Leaf_scorch': 'Apply fungicides containing captan or thiophanate-methyl.',
    'Strawberry___healthy': 'No pesticide needed, plant is healthy.',
    'Tomato___Bacterial_spot': 'Use copper-based bactericides and avoid overhead watering.',
    'Tomato___Early_blight': 'Apply chlorothalonil or mancozeb fungicides.',
    'Tomato___Late_blight': 'Use fungicides like metalaxyl or chlorothalonil.',
    'Tomato___Leaf_Mold': 'Apply fungicides such as copper oxychloride.',
    'Tomato___Septoria_leaf_spot': 'Use chlorothalonil or mancozeb fungicides.',
    'Tomato___Spider_mites Two-spotted_spider_mite': 'Use miticides or insecticidal soaps.',
    'Tomato___Target_Spot': 'Apply fungicides like chlorothalonil or mancozeb.',
    'Tomato___Tomato_Yellow_Leaf_Curl_Virus': 'Control whitefly vector and remove infected plants.',
    'Tomato___Tomato_mosaic_virus': 'Remove infected plants and use resistant varieties.',
    'Tomato___healthy': 'No pesticide needed, plant is healthy.'
}

@app.route('/')
def serve_index():
    # Serve index.html from current directory
    return send_from_directory('.', 'index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    try:
        upload_folder = 'uploads'
        os.makedirs(upload_folder, exist_ok=True)
        img_path = os.path.join(upload_folder, file.filename)
        file.save(img_path)

        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        predictions = model.predict(img_array)[0]  # Get predictions for this image

        top_idx = np.argmax(predictions)
        confidence = float(predictions[top_idx] * 100)

        predicted_class = class_names[top_idx]
        pesticide = pesticide_dict.get(predicted_class, "No pesticide suggestion available.")

        os.remove(img_path)

        return jsonify({
            'disease': predicted_class,
            'confidence': round(confidence, 2),
            'pesticide': pesticide
        })

    except Exception as e:
        if os.path.exists(img_path):
            os.remove(img_path)
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
