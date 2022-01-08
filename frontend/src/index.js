import React from 'react';
import ReactDOM from 'react-dom';
import { createBrowserHistory } from 'history';
import { BrowserRouter as Router, Redirect, Route, Switch } from 'react-router-dom'
import reportWebVitals from './reportWebVitals';
import "./index.css";

//import layout
import LayoutPage from "./layouts/layout"

const history = createBrowserHistory();

ReactDOM.render(
    <Router history={history}>
      <Switch>
        <Route path="/" component={LayoutPage} />
      </Switch>
      <Redirect  from="/" to="/home" />
    </Router>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
