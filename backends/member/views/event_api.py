from django.views.decorators.http import require_POST

from commonlib import eventlib
from commonlib.auth import require_auth
from commonlib.core import validate_schema, SuccessResponse
from commonlib.errors import InvalidRequestParams

MAX_DAY_RANGE = 90

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
def get_event_detail(request, args):
	event_id = args['id']
	event = eventlib.get_event_by_id(event_id)
	if not event:
		raise InvalidRequestParams('Invalid event id')

	images = eventlib.get_images_of_event(event_id)
	tag_ids = eventlib.get_event_tag_ids(event_id)
	tag_names = eventlib.get_tag_names(tag_ids)

	event['images'] = images
	event['tags'] = tag_names

	return SuccessResponse(event)


search_schema = {
	'type': 'object',
	'properties': {
		'start_date': {'type': 'integer', 'minimum': 0},
		'end_date': {'type': 'integer', 'minimum': 0},
		'tag': {'type': 'string'}
	},
	'required': ['start_date', 'end_date', 'tag']
}


@require_POST
@require_auth('member')
@validate_schema(search_schema)
def search_event(request, args):
	start_date = args['start_date']
	end_date = args['end_date']
	tag = args['tag']

	if start_date > end_date:
		raise InvalidRequestParams('Start date is greater than end date')

	if end_date - start_date > MAX_DAY_RANGE * 86400:
		raise InvalidRequestParams('Search range is too large')

	date_filter_event_ids = eventlib.get_event_ids_in_date_range(start_date, end_date)

	if tag != '':
		tag_id = eventlib.get_tag_id_by_name(tag)
		if not tag_id:
			return SuccessResponse({'ids': []})
		tag_filter_event_ids = eventlib.get_event_ids_have_tag_id(tag_id)
		event_ids = list(set(date_filter_event_ids).intersection(set(tag_filter_event_ids)))
	else:
		event_ids = date_filter_event_ids

	list.sort(event_ids, reverse=True)
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
def get_event_infos(request, args):
	ids = args['ids']
	events = eventlib.get_event_infos(ids)
	return SuccessResponse({
		'events': events
	})
