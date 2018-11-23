from commonlib.models import UserTab
from django.forms.models import model_to_dict

from django.core.cache import cache


def cache_user_by_id(id):
	try:
		user = model_to_dict(UserTab.objects.get(id=id))
	except UserTab.DoesNotExist:
		return None

	cache.set('user_id_' + str(id), user)
	return user


def get_user_by_id(id):
	user = cache.get('user_id_' + str(id))
	if user:
		return user
	return cache_user_by_id(id)


def cache_user_by_username(username):
	try:
		user = model_to_dict(UserTab.objects.get(username=username))
	except UserTab.DoesNotExist:
		return None

	cache.set('user_username_' + username, user)
	return user


def get_user_by_username(username):
	user = cache.get('user_username_' + username)
	if user:
		return user
	return cache_user_by_username(username)


def cache_user_by_email(email):
	try:
		user = model_to_dict(UserTab.objects.get(email=email))
	except UserTab.DoesNotExist:
		return None

	cache.set('user_email_' + email, user)
	return user


def get_user_by_email(email):
	user = cache.get('user_email_' + email)
	if user:
		return user
	return cache_user_by_email(email)


def create_user(data):
	user = UserTab.objects.create(**data)
	return model_to_dict(user)


def update_profile(user_id, data):
	user = UserTab.objects.get(id=user_id)
	for key, value in data.iteritems():
		setattr(user, key, value)
	user.save()
	cache_user_by_id(user.id)
	cache_user_by_email(user.email)
	cache_user_by_username(user.username)
	return model_to_dict(user)


def get_user_list(ids):
	users = list(UserTab.objects.filter(id__in=ids).values('id', 'username', 'fullname', 'avatar_path'))
	return users
