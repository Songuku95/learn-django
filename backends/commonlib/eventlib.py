import time

from django.core.cache import cache
from django.forms.models import model_to_dict

from commonlib.cachelib import get_many, get_one
from commonlib.constant import CachePrefix
from commonlib.models import EventTab, ImageTab, TagTab, EventTagTab


def create_event(data):
	event = EventTab.objects.create(**data)
	return model_to_dict(event)


def update_event(event_id, data):
	event = EventTab.objects.get(id=event_id)
	for key, value in data.iteritems():
		if key in ['title', 'description', 'start_date', 'end_date', 'address', 'latitude', 'longitude', 'status']:
			setattr(event, key, value)
	event.save()
	cache.delete(CachePrefix.EVENT_DETAIL + str(event_id))


def add_images_to_event(paths, event_id):
	for path in paths:
		ImageTab.objects.create(
			path=path,
			event_id=event_id
		)
	cache.delete(CachePrefix.EVENT_IMAGES + str(event_id))


@get_one(CachePrefix.EVENT_IMAGES)
def get_images_of_event(event_id):
	images = list(ImageTab.objects.filter(event_id=event_id).values('id', 'path'))
	return images


@get_one(CachePrefix.TAG_BY_NAME)
def get_or_create_tag(name):
	tag = TagTab.objects.get_or_create(name=name)[0]
	return model_to_dict(tag)


def add_tags_to_event(tag_ids, event_id):
	for id in tag_ids:
		EventTagTab.objects.create(event_id=event_id, tag_id=id)
	cache.delete(CachePrefix.EVENT_TAGS + str(event_id))


def delete_tags_from_event(tag_ids, event_id):
	for id in tag_ids:
		EventTagTab.objects.get(event_id=event_id, tag_id=id).delete()
	cache.delete(CachePrefix.EVENT_TAGS + str(event_id))


def update_image_status(id, status):
	try:
		image = ImageTab.objects.get(id=id)
	except ImageTab.DoesNotExist:
		return None
	image.status = status
	image.save()
	return model_to_dict(image)


@get_one(CachePrefix.EVENT_DETAIL)
def get_event(id):
	try:
		event = model_to_dict(EventTab.objects.get(id=id))
	except EventTab.DoesNotExist:
		return None
	return event


def get_event_tag_ids(event_id):
	tag_ids = EventTagTab.objects.filter(event_id=event_id).values_list('tag_id', flat=True)
	return tag_ids


@get_one(CachePrefix.EVENT_TAGS)
def get_event_tags(event_id):
	tag_ids = list(EventTagTab.objects.filter(event_id=event_id).values_list('tag_id', flat=True))
	tag_names = list(TagTab.objects.filter(id__in=tag_ids).values_list('name', flat=True))
	return tag_names


@get_one(CachePrefix.TAG_BY_NAME)
def get_tag_id(name):
	try:
		tag_id = TagTab.objects.get(name=name).id
	except TagTab.DoesNotExist:
		return None
	return tag_id


@get_many(CachePrefix.EVENT_DETAIL)
def get_events(event_ids):
	events = EventTab.objects.filter(id__in=event_ids).all()
	values = {}
	for event in events:
		values[event.id] = model_to_dict(event)
	return values


def get_active_event_ids():
	now = int(time.time())
	event_ids = list(EventTab.objects.filter(start_date__lte=now, end_date__gte=now).values_list('id', flat=True))
	return event_ids


def get_event_ids_in_date_range(start_date, end_date):
	ids = list(EventTab.objects.filter(start_date__gte=start_date, end_date__lte=end_date).values_list('id', flat=True))
	return ids


def get_event_ids_have_tag_id(tag_id):
	event_ids = list(EventTagTab.objects.filter(tag_id=tag_id).values_list('event_id', flat=True))
	return event_ids
