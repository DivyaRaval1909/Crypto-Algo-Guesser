import React from 'react';
import CipherForm from './components/CipherForm';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>🔐 Cryptographic Algorithm Guesser</h1>
        <p>Upload ciphertext and let our ML model predict the encryption algorithm</p>
      </header>
      <main>
        <CipherForm />
      </main>
      <footer>
        <p>Built with React, Node.js, and Python Flask • Workshop Project</p>
      </footer>
    </div>
  );
}

export default App; 