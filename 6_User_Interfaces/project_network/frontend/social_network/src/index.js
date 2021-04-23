import React from 'react';
import ReactDOM from 'react-dom';
import App from './main/App';

ReactDOM.render(
    // StrictMode activates additional checks and warnings.
    <React.StrictMode>
        <App />
    </React.StrictMode>,
    document.getElementById('root')
);
