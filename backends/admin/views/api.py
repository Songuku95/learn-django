from django.views.decorators.http import require_POST

from commonlib import eventlib
from commonlib.auth import require_auth
from commonlib.constant import CommonStatus
from commonlib.core import validate_schema, SuccessResponse
from commonlib.errors import InvalidRequestParams

create_event_schema = {
	'type': 'object',
	'properties': {
		'title': {'type': 'string', 'maxLength': 100},
		'description': {'type': 'string', 'maxLength': 10000},
		'start_date': {'type': 'integer', 'minimum': 0},
		'end_date': {'type': 'integer', 'minimum': 0},
		'address': {'type': 'string', 'maxLength': 200},
		'latitude': {'type': 'number', 'minimum': -90, 'maximum': 90},
		'longitude': {'type': 'number', 'minimum': -180, 'maximum': 180},
		'image_paths': {
			'type': 'array',
			'items': {'type': 'string', 'maxLength': 100},
			'uniqueItems': True,
			'maxItems': 100
		},
		'tags': {
			'type': 'array',
			'items': {'type': 'string', 'maxLength': 20},
			'uniqueItems': True,
			'maxItems': 10
		}
	},
	'required': ['title', 'description', 'start_date', 'end_date', 'address', 'latitude', 'longitude'],
	'additionalProperties': False
}


@require_POST
@require_auth('admin')
@validate_schema(create_event_schema)
def create_event(request, args):
	start_date = args['start_date']
	end_date = args['end_date']

	if start_date > end_date:
		raise InvalidRequestParams('Start date is greater than end date')

	image_paths = args.get('image_paths', [])
	tags = args.get('tags', [])

	event = eventlib.create_event({
		'title': args['title'],
		'description': args['description'],
		'start_date': start_date,
		'end_date': end_date,
		'address': args['address'],
		'latitude': args['latitude'],
		'longitude': args['longitude'],
		'user_id': request.user_id
	})

	print event
	eventlib.add_images_to_event(image_paths, event['id'])
	tag_ids = [eventlib.get_or_create_tag(tag)['id'] for tag in tags]

	eventlib.add_tags_to_event(tag_ids, event['id'])

	return SuccessResponse({
		'id': event['id']
	})


update_event_image_schema = {
	'type': 'object',
	'properties': {
		'image_id': {'type': 'integer', 'minimum': 1},
		'status': {'type': 'integer', 'enum': CommonStatus.get_list()}
	},
	'required': ['image_id', 'status']
}


@require_POST
@require_auth('admin')
@validate_schema(update_event_image_schema)
def update_image_status(request, args):
	image = eventlib.update_image_status(args['image_id'], args['status'])
	if not image:
		raise InvalidRequestParams('Image does not exist')
	return SuccessResponse({})


edit_event_schema = {
	'type': 'object',
	'properties': {
		'id': {'type': 'integer', 'minimum': 1},
		'title': {'type': 'string', 'maxLength': 100},
		'description': {'type': 'string', 'maxLength': 10000},
		'start_date': {'type': 'integer', 'minimum': 0},
		'end_date': {'type': 'integer', 'minimum': 0},
		'address': {'type': 'string', 'maxLength': 200},
		'latitude': {'type': 'number', 'minimum': -90, 'maximum': 90},
		'longitude': {'type': 'number', 'minimum': -180, 'maximum': 180},
		'tags': {
			'type': 'array',
			'items': {'type': 'string', 'maxLength': 20},
			'uniqueItems': True,
			'maxItems': 10
		},
		'status': {'type': 'integer', 'enum': CommonStatus.get_list()}
	},
	'required': ['id', 'title', 'description', 'start_date', 'end_date',
	             'address', 'latitude', 'longitude', 'status'],
	'additionalProperties': False
}


@require_POST
@require_auth('admin')
@validate_schema(edit_event_schema)
def update_event(request, args):
	start_date = args['start_date']
	end_date = args['end_date']
	tags = args.get('tags', [])
	event_id = args['id']

	if start_date > end_date:
		raise InvalidRequestParams('Start date is greater than end date')

	event = eventlib.get_event_by_id(event_id)
	if not event:
		raise InvalidRequestParams('Event does not exist')

	eventlib.update_event(event_id, args)

	current_tag_ids = eventlib.get_event_tag_ids(event_id)
	new_tag_ids = [eventlib.get_or_create_tag(tag)['id'] for tag in tags]
	add_tag_ids = list(set(new_tag_ids) - set(current_tag_ids))
	delete_tag_ids = list(set(current_tag_ids) - set(new_tag_ids))
	eventlib.add_tags_to_event(add_tag_ids, event_id)
	eventlib.delete_tags_from_event(delete_tag_ids, event_id)

	return SuccessResponse({})


add_images_schema = {
	'type': 'object',
	'properties': {
		'event_id': {'type': 'integer', 'minimum': 1},
		'paths': {
			'type': 'array',
			'items': {'type': 'string', 'maxLength': 100},
			'uniqueItems': True,
			'maxItems': 100
		},
	},
	'required': ['paths', 'event_id']
}


@require_POST
@require_auth('admin')
@validate_schema(add_images_schema)
def add_images_to_event(request, args):
	paths = args['paths']
	event_id = args['event_id']

	event = eventlib.get_event_by_id(event_id)
	if not event:
		raise InvalidRequestParams('Event does not exist')

	eventlib.add_images_to_event(paths, event_id)
	return SuccessResponse({})
