class ErrorCodes:
	INVALID_REQUEST_PARAMETERS = 'Invalid request parameters'
	USER_EXIST = 'User already exists'
	SERVER_ERROR = 'Server error'


class ErrorSchema(Exception):
	error_code = ''
	error_message = ''


class ServerError(ErrorSchema):
	error_code = ErrorCodes.SERVER_ERROR


class InavlidRequestParams(ErrorSchema):
	error_code = ErrorCodes.INVALID_REQUEST_PARAMETERS

	def __init__(self, message):
		self.error_message = message


class UserExist(ErrorSchema):
	error_code = ErrorCodes.USER_EXIST
