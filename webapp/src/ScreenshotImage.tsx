import React from 'react';
import './App.css';

function ScreenshotImage() {

  var linkAddress = document.getElementById("redirect_location")?.getAttribute("href");
  if (linkAddress === undefined || linkAddress === null) {
    linkAddress = "https://example.com/path";
  }
  var linkUrl = new URL(linkAddress);
  return <img src={"/page_cache/" + linkUrl.host + btoa(linkUrl.pathname) + ".png"} />;

}

export default ScreenshotImage;
