import CaseConverter from 'utils/caseConverter';

export default ({ dispatch, getState }) => next => (action) => {
  if (!action.promise) {
    return next(action);
  }

  const { promise, type, callback, ...rest } = action;

  const beginAction = type;
  const successAction = `${type}_SUCCESS`;
  const failureAction = `${type}_FAILURE`;

  // Dispatch begin async request action
  next({ type: beginAction, ...rest });

  let p = promise;
  if (typeof promise === 'function') {
    p = promise(dispatch, getState);
  }

  return p.then((response) => {
    if (response.result === 'error') {
      alert(response.errorCode);
    }

    // Dispatch async request success action
    next({
      type: successAction,
      payload: response.reply,
      options: CaseConverter.snakeCaseToCamelCase(rest.payload),
    });

    return response;
  }).catch((error) => {
    console.log('async request fail', error);

    // Dispatch async request failure action
    next({
      type: failureAction,
      payload: error,
      options: CaseConverter.snakeCaseToCamelCase(rest.payload),
    });

    // For showing error message
    next({
      type: 'APP_MESSAGE',
      payload: {
        type: 'error',
        error,
      },
    });

    // Pass error to action via callback
    const response = { success: false, error };
    callback && callback(response, dispatch, getState);
    return response;
  });
};
