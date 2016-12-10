import React from 'react';
import {render} from 'react-dom';
import { Provider } from 'react-redux';
import { createStore, compose, applyMiddleware } from 'redux';
import thunkMiddleware from 'redux-thunk';

import FileUpload from './components/FileUpload';
import rootReducer from './reducers';

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

class App extends React.Component {
  render () {
    return (
      <FileUpload />
    );
  }
}

render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById('app'));
