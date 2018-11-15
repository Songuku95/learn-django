import React from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import configStore from 'store/configStore';
import App from 'components/App';

import { unregister } from './serviceWorker';

const preloadedState = { };
const store = configStore(preloadedState);

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById('root'),
);

unregister();
