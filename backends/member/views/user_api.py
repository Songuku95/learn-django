import uuid

from django.core.files.storage import FileSystemStorage
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_safe

from commonlib import auth, userlib, constant
from commonlib.auth import require_auth
from commonlib.core import validate_schema, SuccessResponse
from commonlib.errors import UserExist, WrongUsernameOrPassword, InvalidRequestParams, FileTooLarge

MAX_IMAGE_FILE_SIZE = 4 * 1024 * 1024

ALLOWED_EXTENSIONS = ['jpg', 'png', 'jpeg']

EMAIL_REGEX = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'


@require_POST
def pre_signup(request):
	password_salt = auth.generate_password_salt()
	verify_code = auth.generate_verify_code()
	return SuccessResponse({
		'password_salt': password_salt,
		'verify_code': verify_code
	})


signup_schema = {
	'type': 'object',
	'properties': {
		'email': {'type': 'string', 'maxLength': 50, 'pattern': EMAIL_REGEX},
		'username': {'type': 'string', 'minLength': 6, 'maxLength': 20, 'pattern': '^\S*$'},
		'password_salt': {'type': 'string'},
		'verify_code': {'type': 'string'},
		'encrypted_password': {'type': 'string'}
	},
	'required': ['email', 'username', 'password_salt', 'verify_code', 'encrypted_password']
}


@require_POST
@validate_schema(signup_schema)
def signup(request, args):
	email = args['email']
	username = args['username']

	# Check whether email and username already exists or not
	if userlib.get_user_by_username(username) or userlib.get_user_by_email(email):
		raise UserExist()

	password_salt = args['password_salt']
	verify_code = args['verify_code']
	encrypted_password = args['encrypted_password']

	# Create new user
	password_hash = auth.get_password_hash(encrypted_password, password_salt, verify_code)
	user = userlib.create_user({
		'email': email,
		'username': username,
		'password_salt': password_salt,
		'password_hash': password_hash
	})

	return SuccessResponse({
		'id': user['id'],
		'token': auth.get_token(user)
	})


pre_login_schema = {
	'type': 'object',
	'properties': {
		'username': {'type': 'string', 'minLength': 6, 'maxLength': 20, 'pattern': '^\S*$'},
	},
	'required': ['username']
}


@require_POST
@validate_schema(pre_login_schema)
def pre_login(request, args):
	username = args['username']
	user = userlib.get_user_by_username(username)
	password_salt = user['password_salt']
	verify_code = auth.generate_verify_code()
	return SuccessResponse({
		'password_salt': password_salt,
		'verify_code': verify_code
	})


login_schema = {
	'type': 'object',
	'properties': {
		'username': {'type': 'string', 'minLength': 6, 'maxLength': 20},
		'encrypted_password': {'type': 'string'},
		'verify_code': {'type': 'string'}
	},
	'required': ['username', 'encrypted_password', 'verify_code']
}


@require_POST
@validate_schema(login_schema)
def login(request, args):
	username = args['username']
	encrypted_password = args['encrypted_password']
	verify_code = args['verify_code']

	user = userlib.get_user_by_username(username)

	if not user:
		raise WrongUsernameOrPassword()

	password_hash = auth.get_password_hash(encrypted_password, user['password_salt'], verify_code)
	if password_hash != user['password_hash']:
		raise WrongUsernameOrPassword()

	return SuccessResponse({
		'token': auth.get_token(user),
		'id': user['id'],
		'email': user['email'],
		'username': user['username'],
		'avatar_path': user['avatar_path'],
		'full_name': user['fullname'],
		'role': user['role']
	})


update_profile_schema = {
	'type': 'object',
	'properties': {
		'fullname': {'type': 'string', 'maxLength': 30},
		'sex': {'type': 'integer', 'enum': [constant.Sex.MALE, constant.Sex.FEMALE]},
		'avatar_path': {'type': 'string', 'maxLength': 100}
	},
	'additionalProperties': False
}


@require_POST
@require_auth('member')
def exchange_token(request):
	user = userlib.get_user_by_id(request.user_id)
	return SuccessResponse({
		'token': auth.get_token(user)
	})


@require_POST
@require_auth('member')
@validate_schema(update_profile_schema)
def update_profile(request, args):
	userlib.update_profile(request.user_id, args)

	return SuccessResponse({})


@require_safe
@require_auth('member')
def get_profile(request):
	user = userlib.get_user_by_id(request.user_id)
	return SuccessResponse({
		'id': user['id'],
		'email': user['email'],
		'username': user['username'],
		'avatar_path': user['avatar_path'],
		'fullname': user['fullname'],
		'role': user['role'],
		'sex': user['sex']
	})


get_user_list_schema = {
	'type': 'object',
	'properties': {
		'ids': {
			'type': 'array',
			'items': {'type': 'integer', 'minimum': 1},
			'uniqueItems': True,
			'maxItems': 100
		}
	},
	'required': ['ids']
}


@require_POST
@require_auth('member')
@validate_schema(get_user_list_schema)
def get_infos(request, args):
	users = userlib.get_user_list(args['ids'])
	result = [{
		'id': user['id'],
		'user_name': user['username'],
		'fullname': user['fullname'],
		'avatar_path': user['avatar_path'],
		'email': user['email']
	} for user in users]
	return SuccessResponse({
		'users': result
	})


@require_POST
@require_auth('member')
def upload_image(request):
	if not request.FILES.get('file'):
		raise InvalidRequestParams('')

	file = request.FILES.get('file')
	if file.size > MAX_IMAGE_FILE_SIZE:
		raise FileTooLarge()

	extension = file.name.split('.')[-1]
	if extension not in ALLOWED_EXTENSIONS:
		raise InvalidRequestParams('File type is not allowed')

	fs = FileSystemStorage()
	filename = fs.save(str(uuid.uuid4()) + '.' + extension, file)
	uploaded_file_path = fs.url(filename)
	return SuccessResponse({
		'image_path': uploaded_file_path
	})
