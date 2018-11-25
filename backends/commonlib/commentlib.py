from django.core.cache import cache
from django.forms.models import model_to_dict

from commonlib.cachelib import get_many, get_one
from commonlib.constant import CachePrefix
from commonlib.models import CommentTab


def create_comment(user_id, event_id, content):
	comment = model_to_dict(CommentTab.objects.create(user_id=user_id, event_id=event_id, content=content))
	comment_ids = cache.get(CachePrefix.COMMENT_IDS + str(event_id))
	if comment_ids is not None:
		comment_ids.append(comment['id'])
		cache.set(CachePrefix.COMMENT_IDS + str(event_id), comment_ids)
	return comment


@get_one(CachePrefix.COMMENT_IDS)
def get_comment_ids_of_event(event_id):
	comment_ids = list(CommentTab.objects.filter(event_id=event_id).values_list('id', flat=True))
	return comment_ids


@get_many(CachePrefix.COMMENT_DETAIL)
def get_comment_infos(comment_ids):
	comments = CommentTab.objects.filter(id__in=comment_ids).all()
	values = {}
	for comment in comments:
		values[comment.id] = model_to_dict(comment)
	return values
