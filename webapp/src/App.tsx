import React from 'react';
import logo from './logo.svg';
import './App.css';
import QRCode from "react-qr-code";

function App() {
  return (
    <div style={{ background: 'white', padding: '16px' }}>
      <QRCode value={document.location.href} />
    </div>
  );
}

export default App;
