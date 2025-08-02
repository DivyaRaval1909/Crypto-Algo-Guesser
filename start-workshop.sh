#!/bin/bash

echo "🔐 Starting Cryptographic Algorithm Guessing Workshop"
echo "=================================================="

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "❌ Port $1 is already in use"
        return 1
    else
        echo "✅ Port $1 is available"
        return 0
    fi
}

# Check ports
echo "🔍 Checking port availability..."
check_port 5001 || exit 1
check_port 4000 || exit 1
check_port 3000 || exit 1

echo ""
echo "🚀 Starting services..."

# Start ML Service (Python Flask)
echo "🐍 Starting ML Service on port 5001..."
cd ml-service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py &
ML_PID=$!
cd ..

# Wait a moment for ML service to start
sleep 3

# Start Backend (Node.js)
echo "🟢 Starting Backend on port 4000..."
cd backend
npm install
npm start &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Start Frontend (React)
echo "⚛️  Starting Frontend on port 3000..."
cd frontend
npm install
npm start &
FRONTEND_PID=$!
cd ..

echo ""
echo "🎉 All services started successfully!"
echo "=================================================="
echo "📊 ML Service:    http://localhost:5001"
echo "🔗 Backend API:   http://localhost:4000"
echo "🌐 Frontend:      http://localhost:3000"
echo ""
echo "💡 Try these example ciphertexts:"
echo "   - 'KHOOR ZRUOG' (Caesar cipher)"
echo "   - 'HELLO WORLD' (plain text)"
echo "   - 'Uryyb Jbeyq' (ROT13)"
echo ""
echo "🛑 Press Ctrl+C to stop all services"
echo ""
echo "💡 If you see any errors, check that Python 3 and Node.js are installed:"
echo "   python3 --version && node --version"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping all services..."
    kill $ML_PID 2>/dev/null
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ All services stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Wait for all background processes
wait 