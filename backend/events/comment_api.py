from django.views.decorators.http import require_POST

from core import validate_schema, SuccessResponse, require_auth
from enums import CommonStatus
from errors import InvalidRequestParams
from events.models import EventTab, CommentTab
from users.models import UserTab

import caches

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
	user = request.user
	event_id = args['event_id']
	content = args['content']
	if not EventTab.objects.filter(id=event_id).exists():
		raise InvalidRequestParams('Invalid id')

	comment = CommentTab.objects.create(event_id=event_id, user_id=user['id'], content=content)
	return SuccessResponse({'id': comment.id})


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
	if not EventTab.objects.filter(id=event_id).exists():
		raise InvalidRequestParams('Invalid id')

	comment_ids = CommentTab.objects.filter(event_id=event_id, status=CommonStatus.ACTIVE).values_list('id', flat=True)
	return SuccessResponse({'comment_ids': list(comment_ids)})


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
	comments = list(CommentTab.objects.filter(id__in=args['ids']).values('id', 'content', 'user_id'))
	for comment in comments:
		user = caches.get_user_by_id(comment['user_id'])
		comment['username'] = user['username']
		comment['fullname'] = user['fullname']
		comment['avatar_path'] = user['avatar_path']
	return SuccessResponse({'comments': comments})


delete_comment_schema = {
	'type': 'object',
	'properties': {
		'id': {'type': 'integer', 'minimum': 1}
	},
	'required': ['id']
}


@require_POST
@require_auth('admin')
@validate_schema(delete_comment_schema)
def delete(request, args):
	comment_id = args['id']
	try:
		comment = CommentTab.objects.get(id=comment_id)
	except CommentTab.DoesNotExist:
		raise InvalidRequestParams('Invalid id')
	comment.status = CommonStatus.DELETED
	comment.save()
	return SuccessResponse({})
