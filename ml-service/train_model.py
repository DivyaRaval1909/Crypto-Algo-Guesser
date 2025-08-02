import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import re

def extract_features_from_text(text):
    """Extract features from ciphertext"""
    if not text:
        return [0, 0, 0, 0]
    
    # Basic features
    length = len(text)
    entropy = calculate_entropy(text)
    
    # Character diversity
    unique_chars = len(set(text))
    char_diversity = unique_chars / length if length > 0 else 0
    
    # Check for common patterns
    has_numbers = bool(re.search(r'\d', text))
    has_uppercase = bool(re.search(r'[A-Z]', text))
    has_lowercase = bool(re.search(r'[a-z]', text))
    has_special = bool(re.search(r'[^A-Za-z0-9\s]', text))
    
    # Pattern score
    pattern_score = sum([has_numbers, has_uppercase, has_lowercase, has_special])
    
    return [length, entropy, char_diversity, pattern_score]

def calculate_entropy(text):
    """Calculate Shannon entropy of text"""
    if not text:
        return 0
    
    freq = {}
    for char in text:
        freq[char] = freq.get(char, 0) + 1
    
    total = len(text)
    entropy = 0
    for count in freq.values():
        probability = count / total
        entropy -= probability * np.log2(probability)
    
    return entropy

def train_model():
    """Train the cryptographic algorithm classifier"""
    
    # Training data
    training_data = [
        ("RIJVSUYVJN", 10, 3.1, 1.0, "Vigenere"),
        ("ZEBBWTBOBW", 10, 3.0, 1.0, "Substitution"),
        ("HWEOLRLLDO", 10, 2.6, 1.0, "Transposition"),
        ("8f9a3b1c0e7d9f4d", 16, 3.9, 0.0, "Modern"),
        # Add more variations for better training
        ("QWERTYUIOP", 10, 3.32, 1.0, "Vigenere"),
        ("ASDFGHJKLZ", 10, 3.32, 1.0, "Vigenere"),
        ("ZXCVBNMASD", 10, 3.32, 1.0, "Vigenere"),
        ("POIUYTREWQ", 10, 3.32, 1.0, "Substitution"),
        ("LKJHGFDSAZ", 10, 3.32, 1.0, "Substitution"),
        ("MNBVCXZLKJ", 10, 3.32, 1.0, "Substitution"),
        ("HELLOWORLD", 10, 2.85, 1.0, "Transposition"),
        ("CRYPTOGRAPHY", 12, 3.08, 1.0, "Transposition"),
        ("ALGORITHM", 9, 2.95, 1.0, "Transposition"),
        ("1a2b3c4d5e6f", 12, 3.58, 0.5, "Modern"),
        ("9f8e7d6c5b4a", 12, 3.58, 0.5, "Modern"),
        ("0x1a2b3c4d5e6f", 14, 3.58, 0.43, "Modern"),
        ("a1b2c3d4e5f6", 12, 3.58, 0.5, "Modern"),
        ("7g8h9i0j1k2l", 12, 3.58, 0.5, "Modern"),
    ]
    
    # Create DataFrame
    df = pd.DataFrame(training_data, columns=['ciphertext', 'length', 'entropy', 'alpha_ratio', 'algorithm'])
    
    # Extract features from ciphertext
    features = []
    for text in df['ciphertext']:
        features.append(extract_features_from_text(text))
    
    # Create feature matrix
    X = np.array(features)
    y = df['algorithm'].values
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"Model Accuracy: {accuracy:.2f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save model
    joblib.dump(model, 'model/crypto_model.pkl')
    print(f"\n✅ Model saved to model/crypto_model.pkl")
    
    # Test predictions
    print("\n🧪 Testing predictions:")
    test_cases = [
        "RIJVSUYVJN",  # Should be Vigenere
        "ZEBBWTBOBW",  # Should be Substitution
        "HWEOLRLLDO",  # Should be Transposition
        "8f9a3b1c0e7d9f4d",  # Should be Modern
    ]
    
    for test_case in test_cases:
        features = extract_features_from_text(test_case)
        prediction = model.predict([features])[0]
        confidence = max(model.predict_proba([features])[0])
        print(f"'{test_case}' → {prediction} (confidence: {confidence:.2f})")
    
    return model

if __name__ == "__main__":
    import os
    
    # Create model directory if it doesn't exist
    os.makedirs('model', exist_ok=True)
    
    print("🤖 Training Cryptographic Algorithm Classifier...")
    model = train_model()
    print("✅ Training completed!") 