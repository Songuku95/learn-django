import { UserAction } from 'constants/action';

const INITIAL_STATE = {
  loggedIn: !!localStorage.getItem('token'),
  id: 0,
  fullname: '',
  sex: -1,
  email: '',
  username: '',
  avatarPath: '',
  role: 0,
};

export default (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case UserAction.SIGNUP_SUCCESS:
    case UserAction.LOGIN_SUCCESS: {
      localStorage.setItem('token', action.payload.token);
      return {
        ...state,
        ...action.payload,
        loggedIn: true,
      };
    }

    case UserAction.GET_PROFILE_SUCCESS:
      return {
        ...state,
        ...action.payload,
      };

    case UserAction.LOGOUT:
      localStorage.clear();
      return {
        ...INITIAL_STATE,
        loggedIn: false,
      };
    default:
      break;
  }
  return state;
};
