import React from 'react';
import {render} from 'react-dom';
import { Provider } from 'react-redux';
import { createStore, compose, applyMiddleware } from 'redux';
import thunkMiddleware from 'redux-thunk';

import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import injectTapEventPlugin from 'react-tap-event-plugin';

// Needed for onTouchTap
// http://stackoverflow.com/a/34015469/988941
injectTapEventPlugin();

import App from './components/App';
import rootReducer from './reducers';
import styles from './styles/main.css';

const middlewares = [
  // Add other middleware on this line...

  // thunk middleware can also accept an extra argument to be passed to each thunk action
  // https://github.com/gaearon/redux-thunk#injecting-a-custom-argument
  thunkMiddleware,
];

const store = createStore(rootReducer, compose(
  applyMiddleware(...middlewares),
  window.devToolsExtension ? window.devToolsExtension() : f => f // add support for Redux dev tools
  )
);

render(
  <MuiThemeProvider>
    <Provider store={store}>
      <App />
    </Provider>
  </MuiThemeProvider>,
  document.getElementById('app'));
