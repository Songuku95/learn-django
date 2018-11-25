from django.core.cache import cache
from django.forms.models import model_to_dict

from commonlib.cachelib import get_one
from commonlib.constant import CachePrefix, CommonStatus
from commonlib.models import EventParticipantTab


def add_participant_to_event(event_id, user_id):
	cache_key = CachePrefix.EVENT_PARTICIPANTS + str(event_id)
	value = cache.get(cache_key)
	if value is not None:
		try:
			value.remove(user_id)
		except ValueError:
			pass
		value.append(user_id)
		cache.set(cache_key, value)


def remove_participant_from_event(event_id, user_id):
	cache_key = CachePrefix.EVENT_PARTICIPANTS + str(event_id)
	value = cache.get(cache_key)
	if value is not None:
		value.remove(user_id)
		cache.set(cache_key, value)


def update(event_id, user_id, status):
	participant, created = EventParticipantTab.objects.get_or_create(event_id=event_id, user_id=user_id)

	participant.status = status
	participant.save()

	if status == CommonStatus.ACTIVE:
		add_participant_to_event(event_id, user_id)
	else:
		remove_participant_from_event(event_id, user_id)
	return model_to_dict(participant)


@get_one(CachePrefix.EVENT_PARTICIPANTS)
def get_participant_ids(event_id):
	participant_ids = list(EventParticipantTab.objects.filter(event_id=event_id).values_list('user_id', flat=True))
	return participant_ids
