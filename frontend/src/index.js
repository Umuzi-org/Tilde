import React from "react";
import ReactDOM from "react-dom/client";
import App from "./components/App";
import * as serviceWorker from "./serviceWorker";
import "typeface-roboto";
import { BrowserRouter as Router } from "react-router-dom";

import { store } from "./redux";
import { Provider } from "react-redux";
const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  //   <React.StrictMode>
  <Provider store={store}>
    <Router>
      <App />
    </Router>
  </Provider>
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
