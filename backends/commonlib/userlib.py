from django.core.cache import cache
from django.forms.models import model_to_dict

from commonlib.cachelib import get_many, get_one
from commonlib.constant import CachePrefix
from commonlib.models import UserTab


@get_one(CachePrefix.USER_DETAIL_BY_ID)
def get_user_by_id(id):
	try:
		user = model_to_dict(UserTab.objects.get(id=id))
	except UserTab.DoesNotExist:
		return None
	return user


@get_one(CachePrefix.USER_DETAIL_BY_USERNAME)
def get_user_by_username(username):
	try:
		user = model_to_dict(UserTab.objects.get(username=username))
	except UserTab.DoesNotExist:
		return None
	return user


@get_one(CachePrefix.USER_DETAIL_BY_EMAIL)
def get_user_by_email(email):
	try:
		user = model_to_dict(UserTab.objects.get(email=email))
	except UserTab.DoesNotExist:
		return None
	return user


def create_user(data):
	user = UserTab.objects.create(**data)
	return model_to_dict(user)


def update_profile(user_id, data):
	user = UserTab.objects.get(id=user_id)
	for key, value in data.iteritems():
		setattr(user, key, value)
	user.save()
	cache.delete(CachePrefix.USER_DETAIL_BY_ID + str(user_id))
	return model_to_dict(user)


@get_many(CachePrefix.USER_DETAIL_BY_ID)
def get_user_list(ids):
	users = UserTab.objects.filter(id__in=ids)
	values = {}
	for user in users:
		values[user.id] = model_to_dict(user)
	return values
