from django.core.cache import cache
from functools import wraps
from django.forms.models import model_to_dict


def get_cache(prefix):
	def get_cache_decorator(f):
		@wraps(f)
		def wrapper_func(key, *args, **kwargs):
			cache_key = prefix + str(key)

			data = cache.get(cache_key)
			if data:
				return data

			value = f(key, *args, **kwargs)
			if value:
				cache.set(cache_key, value)
			return value

		return wrapper_func

	return get_cache_decorator


def update_cache(prefix):
	def get_cache_decorator(f):
		@wraps(f)
		def wrapper_func(key, *args, **kwargs):
			cache_key = prefix + str(key)

			value = f(key, *args, **kwargs)
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
