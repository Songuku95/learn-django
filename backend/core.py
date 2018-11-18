import json
import time
from functools import wraps

from django.db import models
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from jsonschema import validate, ValidationError

import caches
from enums import UserRoleName
from errors import ErrorSchema, InvalidRequestParams, Unauthorized
from users.auth import decode_token


# Reference: https://stackoverflow.com/questions/1737017/django-auto-now-and-auto-now-add
class Model(models.Model):
	created_at = models.PositiveIntegerField(editable=False)
	updated_at = models.PositiveIntegerField()

	def save(self, *args, **kwargs):
		# On saves, update timestamps
		now = int(time.time())
		if not self.id:
			self.created_at = now
		self.updated_at = now
		return super(Model, self).save(*args, **kwargs)

	class Meta:
		abstract = True


class SuccessResponse(JsonResponse):
	def __init__(self, data):
		if not isinstance(data, dict):
			raise TypeError('data must be a dictionary')
		response = {
			'result': 'success',
			'reply': data
		}
		super(SuccessResponse, self).__init__(response)


class ErrorResponse(JsonResponse):
	def __init__(self, data):
		response = {
			'result': 'error',
			'error_code': data.error_code,
			'error_message': data.error_message
		}

		super(ErrorResponse, self).__init__(response)


class ExceptionMiddleware(MiddlewareMixin):
	def process_exception(self, request, exception):
		if isinstance(exception, ErrorSchema):
			return ErrorResponse(exception)
	# return ErrorResponse(ServerError())


def require_auth(role):
	def require_auth_decorator(f):
		@wraps(f)
		def wrapper_func(request, *args, **kwargs):
			token = request.META.get('HTTP_AUTHORIZATION')
			if not token:
				raise Unauthorized()

			# Admin can access API for member
			if role == UserRoleName.ADMIN:
				payload = decode_token(token, UserRoleName.ADMIN)
			elif role == UserRoleName.MEMBER:
				payload = decode_token(token, UserRoleName.ADMIN) or decode_token(token, UserRoleName.MEMBER)
			else:
				raise Unauthorized()

			if not payload:
				raise Unauthorized()

			user = caches.get_user_by_id(payload['sub'])
			if not user:
				raise Unauthorized()

			kwargs['user'] = user
			return f(request, *args, **kwargs)

		return wrapper_func

	return require_auth_decorator


def validate_schema(schema):
	def validate_schema_decorator(f):
		@wraps(f)
		def wrapper_func(request, *args, **kwargs):
			# There are only 2 request methods (GET, POST) because we use require_POST, require_safe in all API
			if request.method == 'GET':
				request_args = request.GET.dict()
			else:
				try:
					request_args = json.loads(request.body)
				except ValueError:
					raise InvalidRequestParams('Wrong request format')

			try:
				validate(request_args, schema)
			except ValidationError as error:
				raise InvalidRequestParams(error.message)

			kwargs['args'] = request_args
			return f(request, *args, **kwargs)

		return wrapper_func

	return validate_schema_decorator
