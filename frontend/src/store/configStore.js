import { createStore, applyMiddleware, compose } from 'redux';

import rootReducer from 'reducers';
import clientMiddleware from './clientMiddleware';

const configureStore = (preloadedState) => {
  // Build the middleware for intercepting and dispatching navigation actions
  const middlewares = [clientMiddleware];

  const store = createStore(
    rootReducer,
    preloadedState,
    compose(
      applyMiddleware(...middlewares),
      window.devToolsExtension()
    ),
  );

  if (module.hot) {
    // Enable Webpack hot module replacement for reducers
    module.hot.accept('../reducers', () => {
      store.replaceReducer(rootReducer);
    });
  }

  return store;
};

export default configureStore;
