import { UserAction } from 'constants/action';
import { get, post, upload } from 'utils/request';

export const login = (username, password) => ({
  type: UserAction.LOGIN,
  promise: post('/user/login/', { username, password }),
});

export const signup = (email, username, password) => ({
  type: UserAction.SIGNUP,
  promise: post('/user/signup/', { email, username, password }),
});

export const getProfile = () => ({
  type: UserAction.GET_PROFILE,
  promise: get('/user/get_profile/'),
});

export const logout = () => ({
  type: UserAction.LOGOUT,
});

export const uploadImage = file => ({
  type: UserAction.UPLOAD_IMAGE,
  promise: upload(file),
});