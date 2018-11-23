from django.core.cache import cache
from django.forms.models import model_to_dict

from commonlib.models import EventLikerTab


def get_or_create_like(event_id, user_id, status):
	like = EventLikerTab.objects.get_or_create(event_id=event_id, user_id=user_id)[0]
	like.status = status
	like.save()
	cache_liker_ids(event_id)
	return model_to_dict(like)


def cache_liker_ids(event_id):
	liker_ids = list(EventLikerTab.objects.filter(event_id=event_id).values_list('user_id', flat=True))
	cache.set('event_likers_' + str(event_id), liker_ids)
	return liker_ids


def get_liker_ids(event_id):
	liker_ids = cache.get('event_likers_' + str(event_id))
	if liker_ids is not None:
		return liker_ids
	return cache_liker_ids(event_id)
