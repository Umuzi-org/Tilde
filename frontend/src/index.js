import React from "react";
import ReactDOM from "react-dom";
import App from "./components/App";
import * as serviceWorker from "./serviceWorker";
import "typeface-roboto";
import { BrowserRouter as Router } from "react-router-dom";

import { store } from "./redux";
import { Provider } from "react-redux";

const LogRocket = require("logrocket");
const setupLogRocketReact = require("logrocket-react");

// only initialize when in the browser
if (typeof window !== "undefined") {
  LogRocket.init("b4pgma/tilde-main");
  // plugins should also only be initialized when in the browser
  setupLogRocketReact(LogRocket);
}

ReactDOM.render(
  //   <React.StrictMode>
  <Provider store={store}>
    <Router>
      <App />
    </Router>
  </Provider>,
  document.getElementById("root")
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
