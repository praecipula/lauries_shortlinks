import React from 'react';
import './App.css';
import QRCode from "react-qr-code";
import ScreenshotImage from './ScreenshotImage';


/* Accepting any props is actually what we want.
 * These are a big ol' bag of props and they might be or mightn't be relevant
 * to any particular component we build.
 * In other words, App is flexible and can, for instance, render different
 * subcomponents depending on the props.
 */
class App extends React.Component<any> {
  render() {
    console.log(this.props);
    return (
      <div>
        <div style={{ background: 'white', padding: '16px' }}>
          <QRCode value={document.location.href} />
        </div>
        <ScreenshotImage />
      </div>
    )
  };
}

export default App;
