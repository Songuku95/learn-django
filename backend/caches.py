from django.core.cache import cache
from functools import wraps
from django.forms.models import model_to_dict
from enums import CommonStatus


def get_cache(prefix):
	def get_cache_decorator(f):
		@wraps(f)
		def wrapper_func(*args, **kwargs):
			if len(args) > 0:
				cache_key = prefix + str(args[0])
			else:
				cache_key = prefix

			data = cache.get(cache_key)
			if data:
				return data

			value = f(*args, **kwargs)
			if value:
				cache.set(cache_key, value)
			return value

		return wrapper_func

	return get_cache_decorator


def update_cache(prefix):
	def get_cache_decorator(f):
		@wraps(f)
		def wrapper_func(*args, **kwargs):
			if len(args) > 0:
				cache_key = prefix + str(args[0])
			else:
				cache_key = prefix

			value = f(*args, **kwargs)
			cache.set(cache_key, value)

			return value

		return wrapper_func

	return get_cache_decorator


@get_cache('user_')
def get_user_by_id(id):
	try:
		from users.models import UserTab
		user = UserTab.objects.values('id', 'username', 'email', 'fullname', 'sex', 'role', 'avatar_path').get(id=id)
	except UserTab.DoesNotExist:
		return None
	return user


@update_cache('user_')
def update_user_by_id(id):
	try:
		from users.models import UserTab
		user = UserTab.objects.values('id', 'username', 'email', 'fullname', 'sex', 'role', 'avatar_path').get(id=id)
	except UserTab.DoesNotExist:
		return None
	return user


@get_cache('event_')
def get_event_by_id(id):
	from events.models import EventTab, EventTagTab, TagTab, ImageTab
	try:
		event = EventTab.objects.get(id=id)
	except EventTab.DoesNotExist:
		return None
	event_tags = EventTagTab.objects.filter(event_id=event.id)
	tag_ids = [event_tag.tag_id for event_tag in event_tags]
	tag_names = [TagTab.objects.get(id=tag_id).name for tag_id in tag_ids]
	images = ImageTab.objects.filter(event_id=event.id)

	event = {
		'created_at': event.created_at,
		'updated_at': event.updated_at,
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
	}
	return event


@update_cache('event_')
def update_event_by_id(id):
	from events.models import EventTab, EventTagTab, TagTab, ImageTab
	try:
		event = EventTab.objects.get(id=id)
	except EventTab.DoesNotExist:
		return None
	event_tags = EventTagTab.objects.filter(event_id=event.id)
	tag_ids = [event_tag.tag_id for event_tag in event_tags]
	tag_names = [TagTab.objects.get(id=tag_id).name for tag_id in tag_ids]
	images = ImageTab.objects.filter(event_id=event.id)

	event = {
		'created_at': event.created_at,
		'updated_at': event.updated_at,
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
	}
	return event


@get_cache('event_active_ids')
def get_all_active_event_ids():
	from events.models import EventTab
	ids = EventTab.objects.filter(status=CommonStatus.ACTIVE).values_list('id', flat=True)
	return list(ids)


@get_cache('event_active_ids')
def update_all_active_event_ids():
	from events.models import EventTab
	ids = EventTab.objects.filter(status=CommonStatus.ACTIVE).values_list('id', flat=True)
	return list(ids)
