import React from 'react';
import './App.css';

class ScreenshotImage extends React.Component {

  fs_location_for_url() {
    //TODO: accept a url instead of introspecting from dom
    var linkAddress = document.getElementById("redirect_location")?.getAttribute("href");
    if (linkAddress === undefined || linkAddress === null) {
      linkAddress = "https://example.com/path";
    }
    var linkUrl = new URL(linkAddress);
    return "/page_cache/" + linkUrl.host + btoa(linkUrl.pathname) + ".png";
  }

  render() {
    return <img src={this.fs_location_for_url()} />
  }

}

export default ScreenshotImage;
