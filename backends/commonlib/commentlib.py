from django.core.cache import cache
from django.forms.models import model_to_dict

from commonlib.models import CommentTab


def create_comment(user_id, event_id, content):
	comment = model_to_dict(CommentTab.objects.create(user_id=user_id, event_id=event_id, content=content))
	cache_comment_ids_of_event(event_id)
	return comment


def cache_comment_ids_of_event(event_id):
	comment_ids = list(CommentTab.objects.filter(event_id=event_id).values_list('id', flat=True))
	cache.set('comment_ids_of_event_' + str(event_id), comment_ids)
	return comment_ids


def get_comment_ids_of_event(event_id):
	comment_ids = cache.get('comment_ids_of_event_' + str(event_id))
	if comment_ids is not None:
		return comment_ids
	return cache_comment_ids_of_event(event_id)


def cache_comment_infos(comment_ids):
	comments = list(CommentTab.objects.filter(id__in = comment_ids).values('id', 'user_id', 'content'))
	cache.set('comment_infos_' + str(comment_ids), comments)
	return comments


def get_comment_infos(comment_ids):
	comments = cache.get('comment_infos_' + str(comment_ids))
	if comments is not None:
		return comments
	return cache_comment_infos(comment_ids)