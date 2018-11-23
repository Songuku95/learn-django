import json
from functools import wraps

from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from jsonschema import validate, ValidationError

from commonlib.errors import ServerError, ErrorSchema, InvalidRequestParams

import logging

import time

request_logger = logging.getLogger('social_event')


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


class LogMiddleware(MiddlewareMixin):
	def process_request(self, request):
		request.start_time = time.time()

	def process_response(self, request, response):
		log_data = {
			'request_path': request.path,
			'elapsed': time.time() - request.start_time,
		}
		if request.content_type == 'application/json':
			request_logger.info('\n' + request.body, extra=log_data)
		else:
			request_logger.info('', extra=log_data)
		return response

	def process_exception(self, request, exception):
		log_data = {
			'request_path': request.path,
			'elapsed': time.time() - request.start_time,
		}
		request_logger.exception('', extra=log_data)
		if isinstance(exception, ErrorSchema):
			return ErrorResponse(exception)
		return ErrorResponse(ServerError())


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
