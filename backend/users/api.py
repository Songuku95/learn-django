from django.db.models import Q
from django.views.decorators.http import require_POST, require_safe, require_http_methods

from core import validate_schema, SuccessResponse, require_auth
from enums import Sex
from errors import UserExist, WrongUsernameOrPassword
from users.auth import generate_password_salt, generate_password_hash, get_token, check_password
from users.models import UserTab

EMAIL_REGEX = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'

signup_schema = {
	'type': 'object',
	'properties': {
		'email': {'type': 'string', 'maxLength': 50, 'pattern': EMAIL_REGEX},
		'username': {'type': 'string', 'minLength': 6, 'maxLength': 20, 'pattern': '^\S*$'},
		'password': {'type': 'string', 'minLength': 8, 'maxLength': 30}
	},
	'required': ['email', 'username', 'password']
}


@require_POST
@validate_schema(signup_schema)
def signup(request, args):
	email = args.get('email')
	username = args.get('username')
	password = args.get('password')

	# Check whether email and username already exists or not
	if UserTab.objects.filter(Q(username__exact=username) | Q(email__exact=email)).exists():
		raise UserExist()

	# Create new user
	password_salt = generate_password_salt()
	password_hash = generate_password_hash(password, password_salt)
	user = UserTab.objects.create(email=email, username=username, password_salt=password_salt,
	                              password_hash=password_hash)

	return SuccessResponse({
		'id': user.id,
		'token': get_token(user)
	})


login_schema = {
	'type': 'object',
	'properties': {
		'username': {'type': 'string', 'minLength': 6, 'maxLength': 20, 'pattern': '^\S*$'},
		'password': {'type': 'string', 'minLength': 8, 'maxLength': 30}
	},
	'required': ['username', 'password']
}


@require_POST
@validate_schema(login_schema)
def login(request, args):
	username = args.get('username')
	password = args.get('password')
	try:
		user = UserTab.objects.get(username=username)
	except UserTab.DoesNotExist:
		raise WrongUsernameOrPassword()
	if not check_password(password, user.password_salt, user.password_hash):
		raise WrongUsernameOrPassword()

	return SuccessResponse({
		'token': get_token(user),
		'id': user.id,
		'email': user.email,
		'username': user.username,
		'avatar_path': user.avatar_path,
		'full_name': user.fullname,
		'role': user.role
	})


update_profile_schema = {
	'type': 'object',
	'properties': {
		'fullname': {'type': 'string', 'maxLength': 30},
		'sex': {'type': 'integer', 'enum': [Sex.MALE, Sex.FEMALE]},
		'avatar_path': {'type': 'string', 'maxLength': 100}
	}
}


@require_POST
@require_auth('member')
@validate_schema(update_profile_schema)
def update_profile(request, user, args):
	for key, value in args.iteritems():
		setattr(user, key, value)
	user.save()
	return SuccessResponse({})


@require_safe
@require_auth('member')
def get_profile(request, user):
	return SuccessResponse({
		'id': user.id,
		'email': user.email,
		'username': user.username,
		'avatar_path': user.avatar_path,
		'fullname': user.fullname,
		'role': user.role,
		'sex': user.sex
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
def get_list(request, user, args):
	ids = args.get('ids')
	users = UserTab.objects.filter(id__in=ids).values('id', 'username', 'fullname', 'avatar_path')
	return SuccessResponse({
		'events': list(users)
	})
