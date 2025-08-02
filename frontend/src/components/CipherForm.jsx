import React, { useState } from 'react';
import axios from 'axios';
import { Search, Loader2, AlertCircle, CheckCircle, Info } from 'lucide-react';
import './CipherForm.css';

function CipherForm() {
  const [ciphertext, setCiphertext] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [algorithms, setAlgorithms] = useState([]);

  // Fetch supported algorithms on component mount
  React.useEffect(() => {
    fetchAlgorithms();
  }, []);

  const fetchAlgorithms = async () => {
    try {
      const response = await axios.get('/api/crypto/algorithms');
      setAlgorithms(response.data.algorithms || []);
    } catch (err) {
      console.error('Failed to fetch algorithms:', err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!ciphertext.trim()) {
      setError('Please enter some ciphertext to analyze');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await axios.post('/api/crypto/guess', { 
        ciphertext: ciphertext.trim() 
      });

      setResult(response.data);
    } catch (err) {
      console.error('Prediction error:', err);
      setError(err.response?.data?.error || 'Failed to predict algorithm. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setCiphertext('');
    setResult(null);
    setError('');
  };

  const getAlgorithmColor = (algorithm) => {
    const colors = {
      'Vigenere': '#666666',
      'Substitution': '#666666',
      'Transposition': '#666666',
      'Modern': '#666666'
    };
    return colors[algorithm] || '#666666';
  };

  return (
    <div className="cipher-form-container">
      <div className="form-card">
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label htmlFor="ciphertext">
              <Search size={20} />
              Enter Ciphertext
            </label>
            <textarea
              id="ciphertext"
              value={ciphertext}
              onChange={(e) => setCiphertext(e.target.value)}
              placeholder="Paste your encrypted text here... (e.g., 'KHOOR ZRUOG' for Caesar cipher)"
              rows="6"
              disabled={loading}
            />
          </div>

          <div className="button-group">
            <button 
              type="submit" 
              disabled={loading || !ciphertext.trim()}
              className="submit-btn"
            >
              {loading ? (
                <>
                  <Loader2 size={18} className="spin" />
                  Analyzing...
                </>
              ) : (
                <>
                  <Search size={18} />
                  Predict Algorithm
                </>
              )}
            </button>
            
            <button 
              type="button" 
              onClick={handleClear}
              className="clear-btn"
              disabled={loading}
            >
              Clear
            </button>
          </div>
        </form>

        {/* Error Display */}
        {error && (
          <div className="error-message">
            <AlertCircle size={18} />
            {error}
          </div>
        )}

        {/* Result Display */}
        {result && (
          <div className="result-card">
            <div className="result-header">
              <CheckCircle size={24} color="#00D4AA" />
              <h3>Prediction Result</h3>
            </div>
            
            <div 
              className="algorithm-badge"
              style={{ backgroundColor: getAlgorithmColor(result.algorithm) }}
            >
              {result.algorithm}
            </div>
            
            <div className="confidence-bar">
              <span>Confidence: {Math.round(result.confidence * 100)}%</span>
              <div className="confidence-progress">
                <div 
                  className="confidence-fill"
                  style={{ width: `${result.confidence * 100}%` }}
                />
              </div>
            </div>

            {/* Algorithm Probability Distribution */}
            {result.algorithm_probabilities && (
              <div className="probability-distribution">
                <h4>Algorithm Probability Distribution</h4>
                <div className="probability-bars">
                  {Object.entries(result.algorithm_probabilities)
                    .sort(([,a], [,b]) => b - a) // Sort by probability descending
                    .map(([algo, prob]) => (
                      <div key={algo} className="probability-bar">
                        <div className="probability-label">
                          <span className="algorithm-name">{algo}</span>
                          <span className="probability-value">{prob}%</span>
                        </div>
                        <div className="probability-progress">
                          <div 
                            className="probability-fill"
                            style={{ 
                              width: `${prob}%`,
                              backgroundColor: getAlgorithmColor(algo)
                            }}
                          />
                        </div>
                      </div>
                    ))}
                </div>
                <div className="total-probability">
                  Total: {Object.values(result.algorithm_probabilities).reduce((sum, prob) => sum + prob, 0)}%
                </div>
              </div>
            )}

            {result.features && (
              <div className="features-grid">
                <div className="feature">
                  <span className="feature-label">Length:</span>
                  <span className="feature-value">{result.features.length}</span>
                </div>
                <div className="feature">
                  <span className="feature-label">Alpha Ratio:</span>
                  <span className="feature-value">{result.features.alpha_ratio ? result.features.alpha_ratio.toFixed(2) : 'N/A'}</span>
                </div>
                <div className="feature">
                  <span className="feature-label">Digit Ratio:</span>
                  <span className="feature-value">{result.features.digit_ratio ? result.features.digit_ratio.toFixed(2) : 'N/A'}</span>
                </div>
                <div className="feature">
                  <span className="feature-label">Symbol Ratio:</span>
                  <span className="feature-value">{result.features.symbol_ratio ? result.features.symbol_ratio.toFixed(2) : 'N/A'}</span>
                </div>
                <div className="feature">
                  <span className="feature-label">Entropy:</span>
                  <span className="feature-value">{result.features.entropy ? result.features.entropy.toFixed(2) : 'N/A'}</span>
                </div>
                <div className="feature">
                  <span className="feature-label">Index of Coincidence:</span>
                  <span className="feature-value">{result.features.ic ? result.features.ic.toFixed(3) : 'N/A'}</span>
                </div>
                <div className="feature">
                  <span className="feature-label">Chi-Square Score:</span>
                  <span className="feature-value">{result.features.chi_square ? result.features.chi_square.toFixed(1) : 'N/A'}</span>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Supported Algorithms */}
        {algorithms.length > 0 && (
          <div className="algorithms-info">
            <div className="info-header">
              <Info size={18} />
              <span>Supported Algorithms</span>
            </div>
            <div className="algorithms-list">
              {algorithms.map((algo, index) => (
                <span 
                  key={index} 
                  className="algorithm-tag"
                  style={{ backgroundColor: getAlgorithmColor(algo) }}
                >
                  {algo}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default CipherForm; 