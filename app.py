from flask import Flask, request, jsonify
from flask_cors import CORS  # Handles cross-origin requests
import os
import random  # For mock predictions

app = Flask(__name__)
CORS(app)  # Enable CORS for the frontend

# List of possible diseases (expand as needed)
diseases = [
    'Tomato Late Blight',
    'Potato Early Blight',
    'Corn Rust',
    'Apple Scab',
    'Grape Black Rot',
    'Healthy'  # Add a healthy option
]

# Pesticide suggestions based on disease (simplified; consult experts)
pesticides = {
    'Tomato Late Blight': 'Copper-based fungicide (e.g., Bordeaux mixture)',
    'Potato Early Blight': 'Chlorothalonil fungicide',
    'Corn Rust': 'Triazole fungicide (e.g., Propiconazole)',
    'Apple Scab': 'Captan fungicide',
    'Grape Black Rot': 'Mancozeb fungicide',
    'Healthy': 'No pesticide needed'
}

def mock_predict_disease():
    # Mock: Randomly pick a disease (replace with real model prediction)
    return random.choice(diseases)

@app.route('/predict', methods=['POST'])
def predict():
    # Check if a file was uploaded
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Save the uploaded file temporarily
    img_path = os.path.join('uploads', file.filename)
    os.makedirs('uploads', exist_ok=True)  # Create folder if it doesn't exist
    file.save(img_path)
    
    try:
        # Mock prediction (in real app, process the image here)
        predicted_disease = mock_predict_disease()
        
        # Get pesticide suggestion
        suggested_pesticide = pesticides.get(predicted_disease, 'Consult an expert')
        
        # Delete the file after processing
        os.remove(img_path)
        
        # Return the result as JSON
        return jsonify({
            'disease': predicted_disease,
            'pesticide': suggested_pesticide
        })
    except Exception as e:
        # Log error and return a message
        print(f"Error: {str(e)}")  # Prints to terminal
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Runs on localhost:5000
