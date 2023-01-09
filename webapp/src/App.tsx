import React from 'react';
import './App.css';
import { QRCode } from 'react-qrcode-logo';


type iQRCCProps = {
  seedContent: string,
  contentUpdate: Function
}

type iQRCCState = {
  content: string;
  renderStatic: boolean
}

class QRCodeContent extends React.Component<iQRCCProps, iQRCCState> {

  constructor(props: any) {
    super(props);
    this.state = {
      content: props.seedContent,
      renderStatic: true
    }
  }

  inputChanged(event: React.ChangeEvent<HTMLInputElement>) {
    console.log("Input changed " + event.currentTarget.value);
    this.setState({content: event.currentTarget.value});
    this.props.contentUpdate(event.currentTarget.value);
  }

  render() {
    var codeText = <p>this.props.seedContent</p>
    if (this.state.renderStatic) {
      codeText = <p id="codeText" style={{width: "100%", textAlign: "center", margin: "0", fontWeight: "700", overflowWrap:"break-word"}}>{this.state.content}</p>
    } else {
      codeText = <input type="text" id="codeText" name="codeText" value={this.state.content} onChange={event=>this.inputChanged(event)}></input>
    }
    return codeText
  }
}

type iAppProps = {
  codeContent?: string,
  iconUrl?: string,
  errorCorrection?: "H" | "M" | "L" | "Q";
}

type iAppState = {
  qrContent: string
}

class App extends React.Component<iAppProps, iAppState> {


  constructor(props: any) {
    super(props);
    var potentialQrContent = document.location.href;
    if (this.props.codeContent) {
      potentialQrContent = this.props.codeContent;
    }
    this.state = {
      qrContent: potentialQrContent
    };
  }

  qrContentUpdated(newContent: string) {
    this.setState({qrContent: newContent});
  }

  render() {
    console.log(this.props);
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
                  <QRCode value={this.state.qrContent}
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
                    <QRCodeContent seedContent={this.state.qrContent} contentUpdate={(newContent: string) => this.qrContentUpdated(newContent)} />
                </div>
    return (
      <div>
        {component}
      </div>
    )
  };
}

export default App;
