from functools import wraps

from django.core.cache import cache


def get_one(prefix):
	def get_one_decorator(f):
		@wraps(f)
		def wrapper_func(key, *args, **kwargs):
			cache_key = prefix + str(key)
			value = cache.get(cache_key)
			if value is not None:
				return value
			value = f(key, *args, **kwargs)
			if value is not None:
				cache.set(cache_key, value)
			return value

		return wrapper_func

	return get_one_decorator


def get_many(prefix):
	def get_many_decorator(f):
		@wraps(f)
		def wrapper_func(keys, *args, **kwargs):
			values = {}
			not_cached_keys = []
			for key in keys:
				cache_key = prefix + str(key)
				value = cache.get(cache_key)
				if value is not None:
					values[key] = value
					continue
				not_cached_keys.append(key)

			not_cached_data = f(not_cached_keys, *args, **kwargs)
			for key, value in not_cached_data.iteritems():
				values[key] = value
				cache_key = prefix + str(key)
				cache.set(cache_key, value)
			return [values[key] for key in keys]

		return wrapper_func

	return get_many_decorator
