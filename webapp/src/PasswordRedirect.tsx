import React, {useEffect} from 'react';
import './App.css';
import sha256 from 'crypto-js/sha256';


function login_and_redirect(password: string, redirect: string) {
    //this is browser crypto
    var hash = sha256(password);
    var url = "/" + hash + "/" + redirect
    console.log(url)

    var request = new XMLHttpRequest()
    request.open('GET', url, true)

    request.onload = function () {
        if (request.status >= 200 && request.status < 400) {
            window.location.href = url
        } else {
          console.log("Incorrect password")
        }
    }
    request.onerror = function () {
        console.log("Request error")
    }
    request.send()
}

interface RedirectProps {
  redirectTo?: string;
  waitTime?: number;
}

function PasswordRedirect(props: RedirectProps) {
  useEffect(() => {
    var waitTime = 5;
      if (props != null && props.waitTime != null) {
        waitTime = props.waitTime;
      }
      setTimeout(() => {
        const password = window.prompt("Please enter your password...", "");
        if (password == null) {
          console.log("Password not returned from prompt")
          return
        }
        if (props != null && props.redirectTo != null) {
          login_and_redirect(password, props.redirectTo)
        } else {
          console.log("Password redirect mounted without data-redirect-to attribute");
        }
      }, waitTime * 1000);
  });
  return (<div />);
}

export default PasswordRedirect;
