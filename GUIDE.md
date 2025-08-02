# 🔐 Cryptographic Algorithm Guessing 


## 🏗️ Architecture Overview

```
┌─────────────────┐    HTTP    ┌─────────────────┐    HTTP    ┌─────────────────┐
│   React Frontend│ ──────────►│  Node.js Backend│ ──────────►│  Python ML Service│
│   (Port 3000)   │            │   (Port 4000)   │            │   (Port 5000)   │
└─────────────────┘            └─────────────────┘            └─────────────────┘
```

### Service Responsibilities:
- **Frontend (React)**: User interface and experience
- **Backend (Node.js)**: API routing and request handling
- **ML Service (Python)**: Machine learning predictions

## 🚀 Quick Start

### Option 1: Automated Startup (Recommended)
```bash
./start-workshop.sh
```

### Option 2: Manual Startup

#### 1. Start ML Service (Python Flask)
```bash
cd ml-service
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

#### 2. Start Backend (Node.js)
```bash
cd backend
npm install
npm start
```

#### 3. Start Frontend (React)
```bash
cd frontend
npm install
npm start
```

## 🧪 Testing the Application

### Example Ciphertexts to Try:

1. **Caesar Cipher (shift by 3)**
   ```
   Input: KHOOR ZRUOG
   Expected: Caesar Cipher
   ```

2. **Plain Text**
   ```
   Input: HELLO WORLD
   Expected: Modern Encryption
   ```

3. **ROT13**
   ```
   Input: Uryyb Jbeyq
   Expected: Substitution Cipher
   ```

4. **Vigenère Cipher**
   ```
   Input: LXFOPVEFRNHR
   Expected: Vigenère Cipher
   ```

## 📚 Learning Objectives

### 1. **Microservices Architecture**
- Understand service separation
- Learn inter-service communication
- Practice API design patterns

### 2. **Full-Stack Development**
- **Frontend**: React hooks, state management, modern UI
- **Backend**: Express.js, middleware, error handling
- **ML Integration**: Python Flask, feature extraction

### 3. **API Communication**
- RESTful API design
- HTTP methods and status codes
- Error handling and validation

### 4. **Modern Development Practices**
- Environment variables
- CORS configuration
- Logging and debugging

## 🔧 Key Technologies

### Frontend
- **React 18**: Modern React with hooks
- **Axios**: HTTP client for API calls
- **Lucide React**: Beautiful icons
- **CSS3**: Modern styling with gradients and animations

### Backend
- **Node.js**: JavaScript runtime
- **Express.js**: Web framework
- **CORS**: Cross-origin resource sharing
- **Axios**: HTTP client for ML service calls

### ML Service
- **Python 3**: Programming language
- **Flask**: Web framework
- **scikit-learn**: Machine learning library
- **Feature Engineering**: Text analysis and statistics

## 🎨 Features Implemented

### Frontend Features
- ✅ Modern, responsive UI with glassmorphism design
- ✅ Real-time form validation
- ✅ Loading states and error handling
- ✅ Beautiful result display with confidence scores
- ✅ Algorithm color coding
- ✅ Feature analysis visualization

### Backend Features
- ✅ RESTful API endpoints
- ✅ Request/response logging
- ✅ Error handling middleware
- ✅ Health check endpoints
- ✅ CORS configuration
- ✅ Environment variable support

### ML Service Features
- ✅ Feature extraction from ciphertext
- ✅ Shannon entropy calculation
- ✅ Character frequency analysis
- ✅ Pattern recognition
- ✅ Confidence scoring
- ✅ Multiple algorithm support

## 🔍 Code Walkthrough

### 1. **Feature Extraction** (`ml-service/utils/feature_extractor.py`)
```python
def extract_features(ciphertext):
    # Calculate text length
    length = len(ciphertext)
    
    # Calculate Shannon entropy
    entropy = shannon_entropy(ciphertext)
    
    # Character diversity
    char_diversity = len(set(ciphertext)) / length
    
    # Pattern analysis
    pattern_score = analyze_patterns(ciphertext)
    
    return [length, entropy, char_diversity, pattern_score]
```

### 2. **API Controller** (`backend/controllers/cryptoController.js`)
```javascript
export const guessAlgorithm = async (req, res) => {
    const { ciphertext } = req.body;
    
    // Call ML service
    const response = await axios.post(`${ML_SERVICE_URL}/predict`, { 
        ciphertext 
    });
    
    res.json(response.data);
};
```

### 3. **React Component** (`frontend/src/components/CipherForm.jsx`)
```jsx
const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
        const response = await axios.post('/api/crypto/guess', { 
            ciphertext: ciphertext.trim() 
        });
        setResult(response.data);
    } catch (err) {
        setError(err.response?.data?.error);
    } finally {
        setLoading(false);
    }
};
```

## 🛠️ Customization Ideas

### 1. **Add More Algorithms**
- Implement actual cryptographic algorithms
- Add more sophisticated ML models
- Include frequency analysis

### 2. **Enhanced UI Features**
- Add dark mode toggle
- Implement ciphertext history
- Add algorithm explanations

### 3. **Advanced ML Features**
- Train on real cryptographic data
- Add neural network models
- Implement ensemble methods

### 4. **Backend Enhancements**
- Add user authentication
- Implement rate limiting
- Add caching layer

## 🐛 Troubleshooting

### Common Issues:

1. **Port Already in Use**
   ```bash
   # Check what's using the port
   lsof -i :3000
   
   # Kill the process
   kill -9 <PID>
   ```

2. **Python Dependencies**
   ```bash
   # Reinstall requirements
   pip install -r requirements.txt --force-reinstall
   ```

3. **Node Modules Issues**
   ```bash
   # Clear npm cache and reinstall
   npm cache clean --force
   rm -rf node_modules package-lock.json
   npm install
   ```

4. **CORS Issues**
   - Check that all services are running
   - Verify CORS configuration in backend
   - Check browser console for errors

## 📖 Additional Resources

- [React Documentation](https://react.dev/)
- [Express.js Guide](https://expressjs.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Cryptography Basics](https://en.wikipedia.org/wiki/Cryptography)
- [Machine Learning Fundamentals](https://scikit-learn.org/stable/)
