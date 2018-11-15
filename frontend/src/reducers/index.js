import { combineReducers } from 'redux';
import user from './user';
import event from './event';

import 'react-datepicker/dist/react-datepicker.css';

const rootReducer = combineReducers({
  user,
  event,
});

export default rootReducer;
