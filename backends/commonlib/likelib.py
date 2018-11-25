from django.core.cache import cache
from django.forms.models import model_to_dict

from commonlib.cachelib import get_one
from commonlib.constant import CachePrefix, CommonStatus
from commonlib.models import EventLikerTab


def add_liker_to_event(event_id, user_id):
	cache_key = CachePrefix.EVENT_LIKERS + str(event_id)
	value = cache.get(cache_key)
	if value is not None:
		try:
			value.remove(user_id)
		except ValueError:
			pass
		value.append(user_id)
		cache.set(cache_key, value)


def remove_liker_from_event(event_id, user_id):
	cache_key = CachePrefix.EVENT_LIKERS + str(event_id)
	value = cache.get(cache_key)
	if value is not None:
		value.remove(user_id)
		cache.set(cache_key, value)


def update(event_id, user_id, status):
	like, created = EventLikerTab.objects.get_or_create(event_id=event_id, user_id=user_id)

	like.status = status
	like.save()

	if status == CommonStatus.ACTIVE:
		add_liker_to_event(event_id, user_id)
	else:
		remove_liker_from_event(event_id, user_id)
	return model_to_dict(like)


@get_one(CachePrefix.EVENT_LIKERS)
def get_liker_ids(event_id):
	liker_ids = list(EventLikerTab.objects.filter(event_id=event_id).values_list('user_id', flat=True))
	return liker_ids
