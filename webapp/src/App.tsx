import React from 'react';
import './App.css';
import QRCode from "react-qr-code";
import ScreenshotImage from './ScreenshotImage';

function App() {
  return (
    <div>
      <div style={{ background: 'white', padding: '16px' }}>
        <QRCode value={document.location.href} />
      </div>
      <div>
        <ScreenshotImage />
      </div>
    </div>
  );
}

export default App;
