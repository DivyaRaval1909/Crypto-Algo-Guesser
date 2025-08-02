# 🔐 Cryptographic Algorithm Guessing Tool

A MERN stack application that uses machine learning to predict cryptographic algorithms from ciphertext.

## 🏗️ Architecture

- **Frontend (View)**: React.js - User Interface
- **Backend (Controller)**: Node.js (Express) - API routing & request handling  
- **ML Service (Model)**: Flask/Python - Loads ML model & predicts algorithm

## 📂 Project Structure

```
crypto-guessing-app/
├── backend/                # Node.js (Controller Layer)
│   ├── controllers/
│   │   └── cryptoController.js
│   ├── routes/
│   │   └── cryptoRoutes.js
│   ├── server.js
│   └── package.json
├── ml-service/             # Python Flask (Model Layer)
│   ├── app.py
│   ├── model/
│   │   └── crypto_model.pkl
│   ├── utils/
│   │   └── feature_extractor.py
│   └── requirements.txt
├── frontend/               # React (View Layer)
│   ├── src/
│   │   ├── components/
│   │   │   └── CipherForm.jsx
│   │   ├── pages/
│   │   │   └── Home.jsx
│   │   └── App.jsx
│   ├── public/
│   └── package.json
└── README.md
```

## 🚀 Quick Start

### 1. Start ML Service (Python Flask)
```bash
cd ml-service
pip install -r requirements.txt
python app.py
# Service will run on http://localhost:5001
```

### 2. Start Backend (Node.js)
```bash
cd backend
npm install
npm start
```

### 3. Start Frontend (React)
```bash
cd frontend
npm install
npm start
```

## 🔧 Technologies Used

- **Frontend**: React.js, Axios
- **Backend**: Node.js, Express, CORS
- **ML Service**: Python, Flask, scikit-learn
- **Communication**: REST APIs

## 🎯 Features

- Upload ciphertext for analysis
- ML-powered algorithm prediction
- Real-time results display
- Clean, modern UI
- Microservices architecture

## 📝 Workshop Learning Objectives

1. **Microservices Architecture**: Understanding service separation
2. **API Communication**: REST APIs between services
3. **ML Integration**: Python Flask serving ML models
4. **Modern Frontend**: React hooks and state management
5. **Full-Stack Development**: Complete application flow 