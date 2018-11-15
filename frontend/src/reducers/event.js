import { EventAction } from 'constants/action';

const INITIAL_STATE = {
  ids: [],
  list: [],
  current: {
    images: [],
    id: 0,
    title: '',
    description: '',
    startDate: '',
    endDate: '',
    latitude: 0,
    longitude: 0,
  },
};

export default (state = INITIAL_STATE, action) => {
  switch (action.type) {
    case EventAction.SEARCH_SUCCESS:
      return {
        ...state,
        ids: action.payload.ids,
      };

    case EventAction.GET_LIST_SUCCESS:
      return {
        ...state,
        list: action.payload.events,
      };

    case EventAction.GET_DETAIL_SUCCESS:
      return {
        ...state,
        current: action.payload,
      };

    default:
      break;
  }
  return state;
};
