import json
import time
from functools import wraps

from django.db import models
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from jsonschema import validate, ValidationError

from enums import ErrorCode, UserRole, UserRoleName
from errors import ErrorSchema, ServerError, InavlidRequestParams, Unauthorized, PermissionDenied
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


class RequestParamsError(ErrorResponse):
	error_code = ErrorCode.INVALID_REQUEST_PARAMETERS

	def __init__(self, message):
		self.error_message = message
		super(RequestParamsError, self).__init__()


class ExceptionMiddleware(MiddlewareMixin):
	def process_exception(self, request, exception):
		if isinstance(exception, ErrorSchema):
			# print exception
			# TODO: log to file
			# return ErrorResponse(ServerError())
			return ErrorResponse(exception)


def require_auth(role):
	def require_auth_decorator(f):
		@wraps(f)
		def wrapper_func(request, *args, **kwargs):
			if role not in UserRoleName.get_list():
				raise PermissionDenied()

			token = request.META.get('HTTP_AUTHORIZATION')
			if not token:
				raise Unauthorized()

			payload = decode_token(token, role)

			# Admin can access API for member
			if role == UserRoleName.ADMIN:
				payload = payload or decode_token(token, UserRoleName.MEMBER)
			if not payload:
				raise PermissionDenied()

			from users.models import UserTab
			try:
				user = UserTab.objects.get(id=payload.get('sub'))
			except UserTab.DoesNotExist:
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
				request_args = json.loads(request.body)

			try:
				validate(request_args, schema)
			except ValidationError as error:
				raise InavlidRequestParams(error.message)

			kwargs['args'] = request_args
			return f(request, *args, **kwargs)

		return wrapper_func

	return validate_schema_decorator
