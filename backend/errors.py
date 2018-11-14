class ErrorCode:
	INVALID_REQUEST_PARAMETERS = 'Invalid request parameters'
	USER_EXIST = 'User already exists'
	SERVER_ERROR = 'Server error'
	WRONG_USERNAME_OR_PASSWORD = 'Wrong username or password'
	UNAUTHORIZED = 'Unauthorized'
	PERMISSION_DENIED = 'Permission denied'


class ErrorSchema(Exception):
	error_code = ''
	error_message = ''


class ServerError(ErrorSchema):
	error_code = ErrorCode.SERVER_ERROR


class Unauthorized(ErrorSchema):
	error_code = ErrorCode.UNAUTHORIZED


class InavlidRequestParams(ErrorSchema):
	error_code = ErrorCode.INVALID_REQUEST_PARAMETERS

	def __init__(self, message):
		self.error_message = message


class UserExist(ErrorSchema):
	error_code = ErrorCode.USER_EXIST


class WrongUsernameOrPassword(ErrorSchema):
	error_code = ErrorCode.WRONG_USERNAME_OR_PASSWORD


class PermissionDenied(ErrorSchema):
	error_code = ErrorCode.PERMISSION_DENIED
