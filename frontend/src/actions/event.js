import { EventAction } from 'constants/action';
import { post } from 'utils/request';

export const createEvent = data => ({
  type: EventAction.CREATE_EVENT,
  promise: post('/event/create/', data),
});

export const updateImageStatus = (imageId, status) => ({
  type: EventAction.UPDATE_IMAGE_STATUS,
  promise: post('/event/image/update/', { imageId, status }),
});

export const updateEvent = data => ({
  type: EventAction.UPDATE_EVENT,
  promise: post('/event/update/', data),
});

export const getEventDetail = id => ({
  type: EventAction.GET_DETAIL,
  promise: post('/event/get_detail/', { id }),
});

export const searchEvent = data => ({
  type: EventAction.SEARCH,
  promise: post('/event/get_ids/', data),
});

export const getEventList = ids => ({
  type: EventAction.GET_LIST,
  promise: post('/event/get_list/', { ids }),
});
