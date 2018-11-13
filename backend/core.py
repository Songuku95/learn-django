import json
from functools import wraps

from django.http import JsonResponse, HttpResponse
from django.utils.deprecation import MiddlewareMixin
from jsonschema import validate, ValidationError

from enums import ErrorCode


class RequestParamsException(Exception):
	def __init__(self, message):
		self.message = message


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
	error_code = ''
	error_message = ''

	def __init__(self):
		response = {
			'result': 'error',
			'error_code': self.error_code,
			'error_message': self.error_message
		}
		super(ErrorResponse, self).__init__(response)


class RequestParamsError(ErrorResponse):
	error_code = ErrorCode.INVALID_REQUEST_PARAMETERS

	def __init__(self, message):
		self.error_message = message
		super(RequestParamsError, self).__init__()


class ExceptionMiddleware(MiddlewareMixin):
	def process_exception(self, request, exception):
		if isinstance(exception, RequestParamsException):
			return RequestParamsError(exception.message)
		return HttpResponse("in exception")


def parse_args_with(schema):
	def parse_args_with_decorator(f):
		@wraps(f)
		def wrapper_func(request, *args, **kwargs):
			request_args = {}

			# There are only 2 request methods (GET, POST) because we use require_POST, require_safe in all API
			if request.method == 'GET':
				request_args = request.GET.dict()
			else:
				request_args = json.loads(request.body)

			try:
				validate(request_args, schema)
			except ValidationError as error:
				raise RequestParamsException(error.message)

			kwargs['args'] = request_args
			return f(request, *args, **kwargs)

		return wrapper_func

	return parse_args_with_decorator
