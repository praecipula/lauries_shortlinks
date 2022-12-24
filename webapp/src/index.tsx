import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import ScreenshotImage from './ScreenshotImage';
import reportWebVitals from './reportWebVitals';

const element = document.getElementById('root')
const root = ReactDOM.createRoot(
   element as HTMLElement
);
const root_attribs = element?.attributes
console.log(root_attribs);
root.render(React.createElement(App, root_attribs));

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
