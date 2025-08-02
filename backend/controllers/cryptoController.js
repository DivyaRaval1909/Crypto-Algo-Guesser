import axios from "axios";

const ML_SERVICE_URL = process.env.ML_SERVICE_URL || "http://localhost:5001";

export const guessAlgorithm = async (req, res) => {
    try {
        const { ciphertext } = req.body;
        
        if (!ciphertext) {
            return res.status(400).json({ 
                error: "Ciphertext is required" 
            });
        }

        console.log(`🔍 Analyzing ciphertext: ${ciphertext.substring(0, 50)}...`);

        // Call ML service
        const response = await axios.post(`${ML_SERVICE_URL}/predict`, { 
            ciphertext 
        });

        console.log(`✅ Prediction received: ${response.data.algorithm}`);

        res.json({
            success: true,
            ...response.data,
            timestamp: new Date().toISOString()
        });

    } catch (error) {
        console.error("❌ Error in crypto controller:", error.message);
        
        if (error.code === 'ECONNREFUSED') {
            return res.status(503).json({ 
                error: "ML prediction service is unavailable",
                details: "Please ensure the ML service is running on port 5000"
            });
        }

        res.status(500).json({ 
            error: "Failed to predict algorithm",
            details: error.message 
        });
    }
};

export const getAlgorithms = async (req, res) => {
    try {
        const response = await axios.get(`${ML_SERVICE_URL}/algorithms`);
        res.json(response.data);
    } catch (error) {
        console.error("❌ Error fetching algorithms:", error.message);
        res.status(500).json({ 
            error: "Failed to fetch supported algorithms" 
        });
    }
};

export const healthCheck = async (req, res) => {
    try {
        // Check ML service health
        const mlHealth = await axios.get(`${ML_SERVICE_URL}/health`);
        
        res.json({
            status: "healthy",
            service: "Crypto Guessing Backend",
            ml_service: mlHealth.data,
            timestamp: new Date().toISOString()
        });
    } catch (error) {
        res.status(503).json({
            status: "unhealthy",
            service: "Crypto Guessing Backend",
            ml_service: "unavailable",
            error: error.message
        });
    }
}; 