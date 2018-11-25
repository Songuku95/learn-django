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


class CommonStatus:
	ACTIVE = 1
	DELETED = 0

	@staticmethod
	def get_list():
		return [CommonStatus.ACTIVE, CommonStatus.DELETED]


class CachePrefix:
	EVENT_DETAIL = 'EVENT_DETAIL'
	EVENT_IMAGES = 'EVENT_IMAGES'
	EVENT_LIKERS = 'EVENT_LIKERS'
	EVENT_PARTICIPANTS = 'EVENT_PARTICIPANTS'
	EVENT_TAGS = 'EVENT_TAG'

	TAG_BY_NAME = 'TAG_BY_NAME'
	TAG_BY_ID = 'TAG_BY_ID'

	USER_DETAIL_BY_ID = 'USER_DETAIL_BY_ID'
	USER_DETAIL_BY_EMAIL = 'USER_DETAIL_BY_EMAIL'
	USER_DETAIL_BY_USERNAME = 'USER_DETAIL_BY_USERNAME'

	COMMENT_DETAIL = 'COMMENT_DETAIL'
	COMMENT_IDS = 'COMMENT_IDS'