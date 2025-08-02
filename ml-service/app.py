from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
from utils.feature_extractor import extract_features
import os

app = Flask(__name__)
CORS(app)

# Load trained ML model
try:
    # Try to load advanced model first
    model = joblib.load("model/advanced_crypto_model.pkl")
    print("✅ Loaded advanced ML model")
    model.algorithms = list(model.classes_)
except FileNotFoundError:
    try:
        # Fallback to basic model
        model = joblib.load("model/crypto_model.pkl")
        print("✅ Loaded basic ML model")
        model.algorithms = list(model.classes_)
    except FileNotFoundError:
        print("⚠️  No trained model found. Using fallback classifier.")
        # Fallback classifier
        class SimpleCryptoClassifier:
            def __init__(self):
                self.algorithms = ['Vigenere', 'Substitution', 'Transposition', 'Modern']
            
            def predict(self, features):
                # Handle both old (4 features) and new (7 features) formats
                if len(features) == 4:
                    length, entropy, diversity, pattern_score = features
                else:
                    length, alpha_ratio, digit_ratio, symbol_ratio, entropy, ic, chi = features
                
                if entropy < 2.0:
                    return 'Substitution'
                elif len(features) == 4 and diversity < 0.3:
                    return 'Vigenere'
                elif len(features) == 7 and alpha_ratio < 0.5:
                    return 'Modern'
                else:
                    return 'Transposition'
            
            def predict_proba(self, features):
                # Return dummy probabilities
                return [[0.25, 0.25, 0.25, 0.25]]
        
        model = SimpleCryptoClassifier()

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "ML Crypto Predictor"})

@app.route("/predict", methods=["POST"])
def predict():
    """Predict cryptographic algorithm from ciphertext"""
    try:
        data = request.json
        ciphertext = data.get("ciphertext", "")
        
        if not ciphertext:
            return jsonify({"error": "No ciphertext provided"}), 400
        
        # Extract features
        features = extract_features(ciphertext)
        
        # Make prediction
        prediction = model.predict([features])[0]
        
        # Get probabilities for all algorithms
        try:
            probabilities = model.predict_proba([features])[0]
            confidence = max(probabilities)
        except:
            # Fallback probabilities
            probabilities = [0.25, 0.25, 0.25, 0.25]
            confidence = 0.25
        
        # Create algorithm probability mapping
        algorithm_probs = {}
        for i, prob in enumerate(probabilities):
            algorithm_probs[model.algorithms[i]] = round(prob * 100, 1)
        
        return jsonify({
            "algorithm": prediction,
            "confidence": round(confidence, 2),
            "algorithm_probabilities": algorithm_probs,
            "features": {
                "length": features[0],
                "alpha_ratio": round(features[1], 2),
                "digit_ratio": round(features[2], 2),
                "symbol_ratio": round(features[3], 2),
                "entropy": round(features[4], 2),
                "ic": round(features[5], 3),
                "chi_square": round(features[6], 1)
            }
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/algorithms", methods=["GET"])
def get_algorithms():
    """Get list of supported algorithms"""
    return jsonify({
        "algorithms": model.algorithms,
        "description": "Supported cryptographic algorithms for prediction"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    print(f"🚀 ML Service starting on port {port}")
    print(f"📊 Available algorithms: {model.algorithms}")
    app.run(host="0.0.0.0", port=port, debug=True) 