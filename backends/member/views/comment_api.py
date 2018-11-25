from django.views.decorators.http import require_POST

from commonlib import commentlib, eventlib
from commonlib.auth import require_auth
from commonlib.core import validate_schema, SuccessResponse
from commonlib.errors import InvalidRequestParams

create_schema = {
	'type': 'object',
	'properties': {
		'event_id': {'type': 'integer', 'minimum': 1},
		'content': {'type': 'string', 'minLength': 1, 'maxLength': 10000},
	},
	'required': ['event_id', 'content']
}


@require_POST
@require_auth('member')
@validate_schema(create_schema)
def create(request, args):
	event_id = args['event_id']
	content = args['content']
	if eventlib.get_event(event_id) is None:
		raise InvalidRequestParams('Event does not exist')

	comment = commentlib.create_comment(request.user_id, event_id, content)

	return SuccessResponse(comment)


get_comment_ids_schema = {
	'type': 'object',
	'properties': {
		'id': {'type': 'integer', 'minimum': 1}
	},
	'required': ['id']
}


@require_POST
@require_auth('member')
@validate_schema(get_comment_ids_schema)
def get_comment_ids(request, args):
	event_id = args['id']

	if eventlib.get_event(event_id) is None:
		raise InvalidRequestParams('Event does not exist')

	comment_ids = commentlib.get_comment_ids_of_event(event_id)
	return SuccessResponse({'comment_ids': comment_ids})


get_comment_details_schema = {
	'type': 'object',
	'properties': {
		'ids': {
			'type': 'array',
			'items': {'type': 'integer', 'minimum': 1},
			'uniqueItems': True,
			'maxItems': 100
		}
	},
	'required': ['ids']
}


@require_POST
@require_auth('member')
@validate_schema(get_comment_details_schema)
def get_comment_details(request, args):
	comment_ids = args['ids']
	return SuccessResponse({'comments': commentlib.get_comment_infos(comment_ids)})
