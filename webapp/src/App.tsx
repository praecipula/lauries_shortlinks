import React from 'react';
import './App.css';
import { QRCode } from 'react-qrcode-logo';


/* Accepting any props is actually what we want.
 * These are a big ol' bag of props and they might be or mightn't be relevant
 * to any particular component we build.
 * In other words, App is flexible and can, for instance, render different
 * subcomponents depending on the props.
 */
class App extends React.Component<any> {

  render() {
    console.log(this.props);
    var qrText = ""
    var caption = ""
    if (this.props.codeContent != null) {
      qrText = this.props.codeContent
      caption = this.props.codeContent
    } else {
      qrText = document.location.href
      caption = ""
    }
    type optionalComponentProps = {
      logoImage?: string
    }
    var optionalLogo : optionalComponentProps = {};
    if (this.props.iconUrl != null) {
      optionalLogo['logoImage'] = this.props.iconUrl
    }
    console.log(optionalLogo)
    var component = <div style={{ height: "400px", width: '320px' }}>
                  <QRCode value={qrText}
                    size={300}
                    qrStyle="dots"
                    ecLevel="H"
                    fgColor="#262626"
                    eyeRadius={[
                      [0, 50, 0, 50],
                      [50, 0, 50, 0],
                      [50, 0, 50, 0]]}
                    eyeColor={[
                      { inner: '#262626',
                        outer: 'darkgreen'
                      },
                      { inner: '#262626',
                        outer: 'darkgreen'
                      },
                      { inner: '#262626',
                        outer: 'darkgreen'
                      },
                      ]}
                      {...optionalLogo}
                      />
                  <p style={{width: "100%", textAlign: "center", margin: "0", fontWeight: "700", overflowWrap:"break-word"}}>{qrText}</p>
                  <canvas id="emoji-rendering-canvas" />
                </div>
    return (
      <div>
        {component}
      </div>
    )
  };
}

export default App;
