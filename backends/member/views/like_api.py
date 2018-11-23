from django.views.decorators.http import require_POST

from commonlib import eventlib, likelib
from commonlib.auth import require_auth
from commonlib.constant import CommonStatus
from commonlib.core import validate_schema, SuccessResponse
from commonlib.errors import InvalidRequestParams

update_schema = {
	'type': 'object',
	'properties': {
		'id': {'type': 'integer', 'minimum': 1},
		'status': {'type': 'integer', 'enum': CommonStatus.get_list()},
	},
	'required': ['id', 'status']
}


@require_POST
@require_auth('member')
@validate_schema(update_schema)
def update_like(request, args):
	user_id = request.user_id
	event_id = args['id']
	status = args['status']

	if not eventlib.get_event_by_id(event_id):
		raise InvalidRequestParams('Event does not exist')

	likelib.get_or_create_like(event_id, user_id, status)

	return SuccessResponse({})


get_event_likers_schema = {
	'type': 'object',
	'properties': {
		'id': {'type': 'integer', 'minimum': 1}
	},
	'required': ['id']
}


@require_POST
@require_auth('member')
@validate_schema(get_event_likers_schema)
def get_event_likers(request, args):
	event_id = args['id']

	if not eventlib.get_event_by_id(event_id):
		raise InvalidRequestParams('Event does not exist')

	liker_ids = likelib.get_liker_ids(event_id)

	return SuccessResponse({'user_ids': liker_ids})
