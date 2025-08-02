import random
import string
import math
import base64
from collections import Counter
import numpy as np
import pandas as pd
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

# ----------------------------
# Feature Extraction Functions
# ----------------------------

def shannon_entropy(text):
    """Calculate Shannon entropy of text"""
    if not text:
        return 0
    freq = {c: text.count(c) for c in set(text)}
    total = len(text)
    return -sum((f/total) * math.log2(f/total) for f in freq.values())

def index_of_coincidence(text):
    """Calculate Index of Coincidence"""
    text = ''.join([c for c in text.upper() if c.isalpha()])
    n = len(text)
    freqs = Counter(text)
    if n <= 1: 
        return 0
    return sum(f*(f-1) for f in freqs.values()) / (n*(n-1))

# English letter frequency distribution
english_freq = {
    'A':8.2,'B':1.5,'C':2.8,'D':4.3,'E':12.7,'F':2.2,'G':2.0,'H':6.1,'I':7.0,'J':0.2,
    'K':0.8,'L':4.0,'M':2.4,'N':6.7,'O':7.5,'P':1.9,'Q':0.1,'R':6.0,'S':6.3,'T':9.1,
    'U':2.8,'V':1.0,'W':2.4,'X':0.2,'Y':2.0,'Z':0.1
}

def chi_square_score(text):
    """Calculate Chi-square statistic against English letter frequencies"""
    text = ''.join([c for c in text.upper() if c.isalpha()])
    total = len(text)
    freq = Counter(text)
    score = 0
    for letter, exp in english_freq.items():
        obs = (freq.get(letter.upper(), 0) / total) * 100 if total > 0 else 0
        score += (obs - exp)**2 / exp
    return score

def extract_features(ciphertext):
    """Extract comprehensive features from ciphertext"""
    if not ciphertext:
        return [0, 0, 0, 0, 0, 0, 0]
    
    length = len(ciphertext)
    alpha_ratio = sum(c.isalpha() for c in ciphertext) / length if length else 0
    digit_ratio = sum(c.isdigit() for c in ciphertext) / length if length else 0
    symbol_ratio = sum(not c.isalnum() for c in ciphertext) / length if length else 0
    entropy = shannon_entropy(ciphertext)
    ic = index_of_coincidence(ciphertext)
    chi = chi_square_score(ciphertext)
    
    return [length, alpha_ratio, digit_ratio, symbol_ratio, entropy, ic, chi]

# ----------------------------
# Encryption Algorithms
# ----------------------------

def vigenere_encrypt(plaintext, key):
    """Vigenère cipher encryption"""
    result = []
    key = key.upper()
    for i, char in enumerate(plaintext.upper()):
        if char.isalpha():
            shift = ord(key[i % len(key)]) - ord('A')
            result.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
        else:
            result.append(char)
    return ''.join(result)

def substitution_encrypt(plaintext):
    """Simple substitution cipher"""
    letters = string.ascii_uppercase
    shuffled = ''.join(random.sample(letters, len(letters)))
    mapping = dict(zip(letters, shuffled))
    return ''.join(mapping.get(c, c) for c in plaintext.upper())

def transposition_encrypt(plaintext, cols=4):
    """Columnar transposition cipher"""
    plaintext = plaintext.replace(" ", "")
    grid = [plaintext[i:i+cols] for i in range(0, len(plaintext), cols)]
    return ''.join(''.join(row[i] for row in grid if i < len(row)) for i in range(cols))

def aes_encrypt(plaintext):
    """AES encryption (simplified for demo)"""
    try:
        key = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_ECB)
        padded = plaintext + (16 - len(plaintext) % 16) * chr(16 - len(plaintext) % 16)
        encrypted = cipher.encrypt(padded.encode())
        return base64.b64encode(encrypted).decode()
    except:
        # Fallback if Crypto library fails
        return base64.b64encode(plaintext.encode()).decode()

# ----------------------------
# Dataset Generation
# ----------------------------

def random_plaintext(length=12):
    """Generate random plaintext for training"""
    words = ["HELLO","WORLD","CRYPTO","SECURE","ATTACK","PASSWORD","MESSAGE","CIPHER",
             "ALGORITHM","ENCRYPTION","DECRYPTION","SECURITY","PRIVACY","AUTHENTICATION"]
    return ' '.join(random.choices(words, k=max(1, length//6)))

def generate_training_data(num_samples=500):
    """Generate comprehensive training dataset"""
    samples = []
    labels = []
    
    print(f"🔄 Generating {num_samples} samples per algorithm...")
    
    for _ in range(num_samples):
        pt = random_plaintext(random.randint(8, 20))
        
        # Vigenère
        ct = vigenere_encrypt(pt, random.choice(["KEY", "SECRET", "CRYPTO", "PASSWORD"]))
        samples.append(extract_features(ct))
        labels.append("Vigenere")
        
        # Substitution
        ct = substitution_encrypt(pt)
        samples.append(extract_features(ct))
        labels.append("Substitution")
        
        # Transposition
        ct = transposition_encrypt(pt, random.randint(3, 6))
        samples.append(extract_features(ct))
        labels.append("Transposition")
        
        # Modern
        ct = aes_encrypt(pt)
        samples.append(extract_features(ct))
        labels.append("Modern")
    
    return samples, labels

# ----------------------------
# ML Training
# ----------------------------

def train_advanced_model():
    """Train the advanced cryptographic classifier"""
    print("🤖 Training Advanced Cryptographic Algorithm Classifier...")
    
    # Generate training data
    samples, labels = generate_training_data(300)  # 300 samples per algorithm = 1200 total
    
    # Create DataFrame
    df = pd.DataFrame(samples, columns=["length","alpha_ratio","digit_ratio","symbol_ratio","entropy","ic","chi_square"])
    X = df.values
    y = np.array(labels)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Train model
    model = RandomForestClassifier(n_estimators=200, random_state=42, max_depth=10)
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"✅ Model Accuracy: {accuracy:.2%}")
    print("\n📊 Classification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save model
    os.makedirs('model', exist_ok=True)
    joblib.dump(model, 'model/advanced_crypto_model.pkl')
    print(f"\n💾 Model saved to model/advanced_crypto_model.pkl")
    
    # Test predictions
    print("\n🧪 Testing predictions:")
    test_cases = [
        ("RIJVSUYVJN", "Vigenere"),
        ("ZEBBWTBOBW", "Substitution"), 
        ("HWEOLRLLDO", "Transposition"),
        ("8f9a3b1c0e7d9f4d", "Modern")
    ]
    
    for test_case, expected in test_cases:
        features = extract_features(test_case)
        prediction = model.predict([features])[0]
        confidence = max(model.predict_proba([features])[0])
        print(f"'{test_case}' → {prediction} (expected: {expected}, confidence: {confidence:.2f})")
    
    return model

if __name__ == "__main__":
    train_advanced_model() 