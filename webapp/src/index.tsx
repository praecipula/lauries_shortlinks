import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import ScreenshotImage from './ScreenshotImage';
// import reportWebVitals from './reportWebVitals';

function mount_standard(class_selector: string, component: React.ComponentClass) {
  document.querySelectorAll(class_selector)
    .forEach(domContainer => {
      const element = domContainer as HTMLElement
      const root_attribs = element.dataset
      const root = ReactDOM.createRoot(element);
      root.render(
        React.createElement(component, root_attribs)
      );
    });
}

function mount_function(class_selector: string, component: React.FunctionComponent) {
  document.querySelectorAll(class_selector)
    .forEach(domContainer => {
      const element = domContainer as HTMLElement
      const root_attribs = element.dataset
      const root = ReactDOM.createRoot(element);
      root.render(
        React.createElement(component, root_attribs)
      );
    });
}

// Now execute the mount process


//CHANGEME
mount_standard(".qrcode-container", App)
mount_standard(".screenshot-container", ScreenshotImage)

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
// reportWebVitals();
