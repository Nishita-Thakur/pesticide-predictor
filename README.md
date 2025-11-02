🌱 AI Plant Disease Predictor (Frontend & Mock Backend)

This repository contains the frontend (index.html) and a mock backend (app.py) for an AI-powered tool designed to predict plant diseases from leaf images and suggest appropriate treatments.

The backend uses Flask to simulate the prediction process, returning random, pre-defined results to allow the frontend to be fully tested and styled.

🚀 Getting Started

Follow these steps to set up and run the application locally on your machine.

Prerequisites

You need a working Python environment to run the backend server.

Python: Ensure Python (version 3.6+) is installed.

pip: Ensure pip (Python package installer) is up to date.

Installation

Navigate to the project directory in your terminal and install the required Python libraries.

Install Dependencies:
This command installs the Flask web framework and the Flask-CORS extension, which is necessary to allow the frontend (index.html) running directly in your browser to communicate with the backend server.

pip install Flask Flask-CORS


🛠️ Running the Application

The application requires two separate processes: the Python backend server and the HTML frontend in your web browser.

Step 1: Run the Backend Server (app.py)

Open your command prompt or terminal and execute the following command:

python app.py


You should see output similar to this, indicating the server is running on port 5000:

 * Running on [http://127.0.0.1:5000/](http://127.0.0.1:5000/) (Press CTRL+C to quit)


Keep this terminal window open while you use the application.

Step 2: Open the Frontend (index.html)

The frontend is a single, self-contained HTML file.

Locate the index.html file in your project folder.

Double-click the file to open it in your preferred web browser (Chrome, Firefox, Edge, etc.).

Usage

In the browser, click the file input area and select an image of a plant leaf (any image will work for this mock version).

Click the "Predict Disease" button.

The frontend will send the image to the running server, and the server will return a randomly selected disease and pesticide suggestion.

📝 Backend Simulation Details

The core logic of the prediction is currently mocked in app.py.

Endpoint: /predict (POST)

Prediction: The mock_predict_disease() function simply selects a random disease from a pre-defined list (Tomato Late Blight, Apple Scab, etc.).

Real-World Upgrade: To make this a functional AI tool, the app.py file would need to be updated to load a real machine learning model (e.g., using TensorFlow/Keras) and process the uploaded image data for actual inference.
