import React from 'react';
import './App.css';
import { QRCode } from 'react-qrcode-logo';


type iQRCCProps = {
  seedContent: string,
  contentUpdate: Function
  renderDynamic: boolean
}

type iQRCCState = {
  content: string;
}

class QRCodeContent extends React.Component<iQRCCProps, iQRCCState> {

  constructor(props: any) {
    super(props);
    this.state = {
      content: props.seedContent,
    }
    console.log(this.props);
  }

  inputChanged(event: React.ChangeEvent<HTMLInputElement>) {
    this.setState({content: event.currentTarget.value});
    this.props.contentUpdate(event.currentTarget.value);
  }

  render() {
    var codeText = <p>this.props.seedContent</p>
    if (this.props.renderDynamic) {
      codeText = <input type="text"
        id="codeText"
        name="codeText"
        value={this.state.content}
        onChange={event=>this.inputChanged(event)}
        style={{width: "100%", textAlign: "center", margin: "0", fontWeight: "700", overflowWrap:"break-word"}}></input>
    } else {
      codeText = <p id="codeText" style={{width: "100%", textAlign: "center", margin: "0", fontWeight: "700", overflowWrap:"break-word"}}>{this.state.content}</p>
    }
    return codeText
  }
}

type iAppProps = {
  codeContent?: string,                     // Initial content for the qr code
  iconUrl?: string,                         // Overlay icon from this location
  errorCorrection?: "L" | "M" | "Q" | "H";  // Error correction for the qr code
  renderDynamic?: "true" | "false";         // Whether the QR code is expected to change. (This will effectively render components to do so).
  style?: "plain" | "matt";                 // Whether the QR code is expected to change. (This will effectively render components to do so).
}

type iAppState = {
  qrContent: string                         // Actual content for the qr code. This can be dynamic.
  renderDynamic: boolean                    // Whether to render the code as editable in the browser.
  errorCorrection: "L" | "M" | "Q" | "H";   // Error correction level
  style: "plain" | "matt";
}

class App extends React.Component<iAppProps, iAppState> {


  constructor(props: any) {
    super(props);
    this.state = {
      qrContent: (this.props.codeContent === undefined) ? "" : this.props.codeContent,
      renderDynamic: (this.props.renderDynamic === undefined) ? false : (this.props.renderDynamic === "true") ? true : false,
      errorCorrection: (this.props.errorCorrection === undefined) ? "Q" : this.props.errorCorrection,
      style: (this.props.style === undefined) ? "plain" : this.props.style
    };
  }

  qrContentUpdated(newContent: string) {
    this.setState({qrContent: newContent});
  }

  render() {
    console.log(this.props);
    type optionalComponentProps = {
      logoImage?: string
    }
    var optionalProps : optionalComponentProps = {};
    if (this.props.iconUrl != null) {
      optionalProps['logoImage'] = this.props.iconUrl;
    }

    type styleProps = {
      size : number
      qrStyle : "squares" | "dots";
      fgColor : string;
      eyeRadius : number;
      eyeColorInner: string;
      eyeColorOuter: string;
    }
    var style : styleProps = {
      size : 300,
      qrStyle : "squares",
      fgColor : "#000000",
      eyeRadius : 0,
      eyeColorInner: "#000000",
      eyeColorOuter: "#000000"
    };
    //fgColor="#262664"

    type errorCorrectionLevel = "H" | "M" | "L" | "Q";
    var errorCorrection: errorCorrectionLevel = "H";
    if (this.props.errorCorrection != null) {
      errorCorrection = this.props.errorCorrection;
    }
    console.log(optionalProps)
    

    var component = <div style={{ height: "400px", width: '320px' }}>
                  <QRCode value={this.state.qrContent}
                    size={style.size}
                    qrStyle={style.qrStyle}
                    fgColor={style.fgColor}
                    eyeRadius={[
                      [style.eyeRadius, 0, style.eyeRadius, 0],
                      [0, style.eyeRadius, 0, style.eyeRadius],
                      [0, style.eyeRadius, 0, style.eyeRadius]]}
                    eyeColor={[
                      { inner: style.eyeColorInner,
                        outer: style.eyeColorOuter
                      },
                      { inner: style.eyeColorInner,
                        outer: style.eyeColorOuter
                      },
                      { inner: style.eyeColorInner,
                        outer: style.eyeColorOuter
                      },
                      ]}
                    logoWidth={200}
                    logoOpacity={0.4}
                    ecLevel={errorCorrection}
                      {...optionalProps}
                      />
                    <QRCodeContent seedContent={this.state.qrContent}
                      contentUpdate={(newContent: string) => this.qrContentUpdated(newContent)}
                      renderDynamic={this.state.renderDynamic}/>
                </div>
    return (
      <div>
        {component}
      </div>
    )
  };
}

export default App;
