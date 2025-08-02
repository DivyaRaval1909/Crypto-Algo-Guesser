import express from "express";
import cors from "cors";
import cryptoRoutes from "./routes/cryptoRoutes.js";
import dotenv from "dotenv";

// Load environment variables
dotenv.config();

const app = express();
const PORT = process.env.PORT || 4000;

// Middleware
app.use(cors({
    origin: process.env.FRONTEND_URL || "http://localhost:3000",
    credentials: true
}));
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Request logging middleware
app.use((req, res, next) => {
    console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
    next();
});

// Routes
app.use("/api/crypto", cryptoRoutes);

// Root endpoint
app.get("/", (req, res) => {
    res.json({
        message: "🔐 Crypto Guessing Backend API",
        version: "1.0.0",
        endpoints: {
            health: "/api/crypto/health",
            algorithms: "/api/crypto/algorithms",
            predict: "/api/crypto/guess"
        }
    });
});

// Error handling middleware
app.use((err, req, res, next) => {
    console.error("❌ Server error:", err);
    res.status(500).json({
        error: "Internal server error",
        message: err.message
    });
});

// 404 handler
app.use("*", (req, res) => {
    res.status(404).json({
        error: "Endpoint not found",
        available_endpoints: [
            "GET /",
            "GET /api/crypto/health",
            "GET /api/crypto/algorithms",
            "POST /api/crypto/guess"
        ]
    });
});

// Start server
app.listen(PORT, () => {
    console.log(`🚀 Backend server running on port ${PORT}`);
    console.log(`📡 API available at http://localhost:${PORT}`);
    console.log(`🔗 ML Service URL: ${process.env.ML_SERVICE_URL || "http://localhost:5001"}`);
    console.log(`🌐 Frontend URL: ${process.env.FRONTEND_URL || "http://localhost:3000"}`);
}); 