from commonlib.models import EventTab, ImageTab, TagTab, EventTagTab, EventLikerTab, EventParticipantTab
from django.forms.models import model_to_dict

from django.core.cache import cache


def create_event(data):
	event = EventTab.objects.create(**data)
	return model_to_dict(event)


def update_event(event_id, data):
	event = EventTab.objects.get(id=event_id)
	for key, value in data.iteritems():
		if key in ['title', 'description', 'start_date', 'end_date', 'address', 'latitude', 'longitude', 'status']:
			setattr(event, key, value)
	event.save()
	cache_event_by_id(event_id)


def add_images_to_event(paths, event_id):
	for path in paths:
		ImageTab.objects.create(
			path=path,
			event_id=event_id
		)
	cache_images_of_event(event_id)


def cache_images_of_event(event_id):
	images = list(ImageTab.objects.filter(event_id=event_id).values('id', 'path'))
	cache.set('event_images_' + str(event_id), images)
	return images


def get_images_of_event(event_id):
	images = cache.get('event_images' + str(event_id))
	if images is not None:
		return images
	return cache_images_of_event(event_id)


def get_or_create_tag(name):
	tag = TagTab.objects.get_or_create(name=name)[0]
	return model_to_dict(tag)


def add_tags_to_event(tag_ids, event_id):
	for id in tag_ids:
		EventTagTab.objects.create(event_id=event_id, tag_id=id)
	cache_event_tag_ids(event_id)


def delete_tags_from_event(tag_ids, event_id):
	for id in tag_ids:
		EventTagTab.objects.get(event_id=event_id, tag_id=id).delete()
	cache_event_tag_ids(event_id)


def update_image_status(id, status):
	try:
		image = ImageTab.objects.get(id=id)
	except ImageTab.DoesNotExist:
		return None
	image.status = status
	image.save()
	return model_to_dict(image)


def cache_event_by_id(id):
	try:
		event = model_to_dict(EventTab.objects.get(id=id))
	except EventTab.DoesNotExist:
		return None
	cache.set('event_id_' + str(id), event)
	return event


def get_event_by_id(id):
	event = cache.get('event_id_' + str(id))
	if event:
		return event
	return cache_event_by_id(id)


def cache_event_tag_ids(event_id):
	tag_ids = EventTagTab.objects.filter(event_id=event_id).values_list('tag_id', flat=True)
	cache.set('event_tag_ids_' + str(event_id), tag_ids)
	return tag_ids


def get_event_tag_ids(event_id):
	tag_ids = cache.get('event_tag_ids_' + str(event_id))
	if tag_ids is not None:
		return tag_ids
	return cache_event_tag_ids(event_id)


def cache_tag_names(tag_ids):
	names = list(TagTab.objects.filter(id__in=tag_ids).values_list('name', flat=True))
	cache.set('tag_names_' + str(tag_ids), names)
	return names


def get_tag_names(tag_ids):
	names = cache.get('tag_names_' + str(tag_ids))
	if names is not None:
		return names
	return cache_tag_names(tag_ids)


def cache_tag_id_by_name(name):
	try:
		tag_id = TagTab.objects.get(name=name).id
	except TagTab.DoesNotExist:
		return None
	cache.set('tag_name_' + name, tag_id)
	return tag_id


def get_tag_id_by_name(name):
	tag_id = cache.get('tag_name_' + name)
	if tag_id:
		return tag_id
	return cache_tag_id_by_name(name)


def get_event_ids_in_date_range(start_date, end_date):
	ids = list(EventTab.objects.filter(start_date__gte=start_date, end_date__lte=end_date).values_list('id', flat=True))
	return ids


def cache_event_ids_have_tag_id(tag_id):
	event_ids = list(EventTagTab.objects.filter(tag_id=tag_id).values_list('event_id', flat=True))
	cache.set('event_ids_have_tag_id_' + str(tag_id), event_ids)
	return event_ids


def get_event_ids_have_tag_id(tag_id):
	event_ids = cache.get('event_ids_have_tag_id_' + str(tag_id))
	if event_ids is not None:
		return event_ids
	return cache_event_ids_have_tag_id(tag_id)


def get_event_infos(event_ids):
	events = list(EventTab.objects.filter(id__in=event_ids).values('id', 'title', 'start_date', 'end_date', 'address'))
	return events
