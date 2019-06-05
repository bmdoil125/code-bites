
import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router } from 'react-router-dom';

import App from './App.jsx'

// Mount App to DOM of HTML element root
ReactDOM.render((
    <Router>
        <App />
    </Router>
), document.getElementById('root'));


