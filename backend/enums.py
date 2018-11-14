class ErrorCode:
	INVALID_REQUEST_PARAMETERS = 'Invalid request parameters'
	USER_EXIST = 'User already exists'


class UserRole:
	MEMBER = 0
	ADMIN = 1


class UserRoleName:
	MEMBER = 'member'
	ADMIN = 'admin'

	@staticmethod
	def get_list():
		return [UserRoleName.MEMBER, UserRoleName.ADMIN]


class Sex:
	MALE = 1
	FEMALE = 0
	PENDING = -1
