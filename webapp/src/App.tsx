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
    if (this.props.codeContent != null) {
      qrText = this.props.codeContent
    } else {
      qrText = document.location.href
    }
    type optionalComponentProps = {
      logoImage?: string
      ecLevel?: "H" | "M" | "L" | "Q";
    }
    var optionalProps : optionalComponentProps = {};
    if (this.props.iconUrl != null) {
      optionalProps['logoImage'] = this.props.iconUrl;
    }
    type errorCorrectionLevel = "H" | "M" | "L" | "Q";
    var errorCorrection: errorCorrectionLevel = "H";
    if (this.props.errorCorrection != null) {
      errorCorrection = this.props.errorCorrection;
    }
    console.log(optionalProps)
    var component = <div style={{ height: "400px", width: '320px' }}>
                  <QRCode value={qrText}
                    size={300}
                    qrStyle="dots"
                    fgColor="#262664"
                    eyeRadius={[
                      [50, 0, 50, 0],
                      [0, 50, 0, 50],
                      [0, 50, 0, 50]]}
                    eyeColor={[
                      { inner: '#262664',
                        outer: '#151515'
                      },
                      { inner: '#262664',
                        outer: '#151515'
                      },
                      { inner: '#262664',
                        outer: '#151515'
                      },
                      ]}
                    logoWidth={200}
                    logoOpacity={0.4}
                    ecLevel={errorCorrection}
                      {...optionalProps}
                      />
                  <p style={{width: "100%", textAlign: "center", margin: "0", fontWeight: "700", overflowWrap:"break-word"}}>{qrText}</p>
                </div>
    return (
      <div>
        {component}
      </div>
    )
  };
}

export default App;
