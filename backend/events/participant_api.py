from django.views.decorators.http import require_POST

from core import validate_schema, SuccessResponse, require_auth
from enums import CommonStatus
from errors import InvalidRequestParams
from events.models import EventTab, EventParticipantTab

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
def update_participant(request, user, args):
	event_id = args.get('id')
	status = args.get('status')
	if not EventTab.objects.filter(id=event_id).exists():
		raise InvalidRequestParams('Invalid id')
	EventParticipantTab.objects.get_or_create(user_id=user.id, event_id=event_id, status=status)
	return SuccessResponse({})


get_event_participants_schema = {
	'type': 'object',
	'properties': {
		'id': {'type': 'integer', 'minimum': 1}
	},
	'required': ['id']
}


@require_POST
@require_auth('member')
@validate_schema(get_event_participants_schema)
def get_event_participants(request, user, args):
	event_id = args.get('id')
	if not EventTab.objects.filter(id=event_id).exists():
		raise InvalidRequestParams('Invalid id')

	user_ids = EventParticipantTab.objects.filter(event_id=event_id, status=CommonStatus.ACTIVE) \
		.values_list('user_id', flat=True)
	return SuccessResponse({'user_ids': list(user_ids)})
