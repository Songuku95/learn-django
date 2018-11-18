from django.views.decorators.http import require_POST, require_safe

from core import validate_schema, SuccessResponse, require_auth
from errors import InvalidRequestParams
from events.models import EventTab, ImageTab, TagTab, EventTagTab

from enums import CommonStatus

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
	'required': ['title', 'description', 'start_date', 'end_date', 'address', 'latitude', 'longitude']
}


@require_POST
@require_auth('admin')
@validate_schema(create_event_schema)
def create_event(request, user, args):
	start_date = args.get('start_date')
	end_date = args.get('end_date')
	image_paths = args.get('image_paths', [])
	tags = args.get('tags', [])

	if start_date > end_date:
		raise InvalidRequestParams('Start date is greater than end date')

	event = EventTab.objects.create(
		title=args.get('title'),
		description=args.get('description'),
		start_date=start_date,
		end_date=end_date,
		address=args.get('address'),
		latitude=args.get('latitude'),
		longitude=args.get('longitude'),
		user_id=user['id'],
	)

	for image_path in image_paths:
		create_image_with_event_id(image_path, event.id)

	tag_ids = [create_or_get_tag_id(tag) for tag in tags]
	for tag_id in tag_ids:
		EventTagTab.objects.create(tag_id=tag_id, event_id=event.id)

	return SuccessResponse({
		'id': event.id
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
def update_image_status(request, user, args):
	try:
		image = ImageTab.objects.get(id=args.get('image_id'))
	except ImageTab.DoesNotExist:
		raise InvalidRequestParams('Invalid image id')
	image.status = args.get('status')
	image.save()
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
	             'address', 'latitude', 'longitude', 'tags', 'status']
}


@require_POST
@require_auth('admin')
@validate_schema(edit_event_schema)
def update_event(request, user, args):
	start_date = args.get('start_date')
	end_date = args.get('end_date')
	tags = args.get('tags')

	if start_date > end_date:
		raise InvalidRequestParams('Start date is greater than end date')

	try:
		event = EventTab.objects.get(id=args.get('id'))
	except EventTab.DoesNotExist:
		raise InvalidRequestParams('Invalid event id')

	event_tags = EventTagTab.objects.filter(event_id=event.id)
	current_tag_ids = [event_tag.id for event_tag in event_tags]
	new_tag_ids = [create_or_get_tag_id(tag) for tag in tags]
	add_tag_ids = list(set(new_tag_ids) - set(current_tag_ids))
	delete_tag_ids = list(set(current_tag_ids) - set(new_tag_ids))

	for tag_id in delete_tag_ids:
		EventTagTab.objects.get(event_id=event.id, tag_id=tag_id).delete()

	for tag_id in add_tag_ids:
		EventTagTab.objects.create(tag_id=tag_id, event_id=event.id)

	event.title = args.get('title')
	event.description = args.get('description')
	event.start_date = start_date
	event.end_date = end_date
	event.address = args.get('address')
	event.latitude = args.get('latitude')
	event.longitude = args.get('longitude')
	event.status = args.get('status')
	event.save()

	return SuccessResponse({})


add_image_schema = {
	'type': 'object',
	'properties': {
		'event_id': {'type': 'integer', 'minimum': 1},
		'path': {'type': 'string', 'maxLength': 100},
	},
	'required': ['path', 'event_id']
}


@require_POST
@require_auth('admin')
@validate_schema(add_image_schema)
def add_image_to_event(request, user, args):
	path = args.get('path')
	event_id = args.get('event_id')

	if not EventTab.objects.filter(id=event_id).exists():
		raise InvalidRequestParams('Invalid event id')

	image_id = create_image_with_event_id(path, event_id)
	return SuccessResponse({'image_id': image_id})


get_event_detail_schema = {
	'type': 'object',
	'properties': {
		'id': {'type': 'integer', 'minimum': 1}
	},
	'required': ['id']
}


@require_POST
@require_auth('member')
@validate_schema(get_event_detail_schema)
def get_event_detail(request, args, user):
	try:
		event = EventTab.objects.get(id=args.get('id'))
	except EventTab.DoesNotExist:
		raise InvalidRequestParams('Invalid event id')

	event_tags = EventTagTab.objects.filter(event_id=event.id)
	tag_ids = [event_tag.tag_id for event_tag in event_tags]
	tag_names = [TagTab.objects.get(id=tag_id).name for tag_id in tag_ids]

	images = ImageTab.objects.filter(event_id=event.id)

	return SuccessResponse({
		'id': event.id,
		'title': event.title,
		'description': event.description,
		'start_date': event.start_date,
		'end_date': event.end_date,
		'address': event.address,
		'latitude': event.latitude,
		'longitude': event.longitude,
		'tags': tag_names,
		'images': list(images.values('id', 'path', 'status'))
	})


search_schema = {
	'type': 'object',
	'properties': {
		'start_date': {'type': 'integer', 'minimum': 0},
		'end_date': {'type': 'integer', 'minimum': 0},
		'tag': {'type': 'string'}
	}
}


@require_POST
@require_auth('member')
@validate_schema(search_schema)
def search_event(request, user, args):
	start_date = args.get('start_date')
	end_date = args.get('end_date')
	tag = args.get('tag')

	date_filter_events = EventTab.objects
	if start_date:
		date_filter_events = date_filter_events.filter(start_date=start_date)
	if end_date:
		date_filter_events = date_filter_events.filter(end_date=end_date)

	date_filter_event_ids = list(date_filter_events.values_list('id', flat=True))

	if tag:
		tag_ids = list(TagTab.objects.filter(name__contains=tag).values_list('id', flat=True))
		tag_filter_event_ids = EventTagTab.objects.filter(tag_id__in=tag_ids)
		tag_filter_event_ids = list(tag_filter_event_ids.values_list('event_id', flat=True).distinct())
	else:
		tag_filter_event_ids = list(EventTab.objects.values_list('id', flat=True))

	event_ids = list(set(date_filter_event_ids).intersection(tag_filter_event_ids))
	return SuccessResponse({'ids': event_ids})


get_event_list_schema = {
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
@validate_schema(get_event_list_schema)
def get_event_list(request, user, args):
	ids = args.get('ids')
	events = EventTab.objects.filter(id__in=ids).values('id', 'title', 'start_date', 'end_date', 'address')
	return SuccessResponse({
		'events': list(events)
	})


def create_image_with_event_id(image_path, event_id):
	image = ImageTab.objects.create(
		path=image_path,
		event_id=event_id
	)
	return image.id


def create_or_get_tag_id(tag_name):
	tag = TagTab.objects.get_or_create(name=tag_name)[0]
	return tag.id
