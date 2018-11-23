from django.core.cache import cache
from django.forms.models import model_to_dict

from commonlib.models import EventParticipantTab


def get_or_create_participant(event_id, user_id, status):
	participant = EventParticipantTab.objects.get_or_create(event_id=event_id, user_id=user_id)[0]
	participant.status = status
	participant.save()
	cache_participant_ids(event_id)
	return model_to_dict(participant)


def cache_participant_ids(event_id):
	participant_ids = list(EventParticipantTab.objects.filter(event_id=event_id).values_list('user_id', flat=True))
	cache.set('event_participant_' + str(event_id), participant_ids)
	return participant_ids


def get_participant_ids(event_id):
	participant_ids = cache.get('event_participants_' + str(event_id))
	if participant_ids is not None:
		return participant_ids
	return cache_participant_ids(event_id)
