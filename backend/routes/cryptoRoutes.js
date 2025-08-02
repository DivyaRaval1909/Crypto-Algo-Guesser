import express from "express";
import { guessAlgorithm, getAlgorithms, healthCheck } from "../controllers/cryptoController.js";

const router = express.Router();

// Health check endpoint
router.get("/health", healthCheck);

// Get supported algorithms
router.get("/algorithms", getAlgorithms);

// Predict cryptographic algorithm
router.post("/guess", guessAlgorithm);

export default router; 