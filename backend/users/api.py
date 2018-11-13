from django.db.models import Q
from django.views.decorators.http import require_POST

from core import validate_schema, SuccessResponse
from errors import UserExist
from users.auth import generate_password_salt, generate_password_hash, get_token
from users.models import UserTab

EMAIL_REGEX = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'

signup_schema = {
	'type': 'object',
	'properties': {
		'email': {'type': 'string', 'maxLength': 50, 'pattern': EMAIL_REGEX},
		'username': {'type': 'string', 'minLength': 6, 'maxLength': 20, 'pattern': '^\w+$'},
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
	user = UserTab.objects.create(email=email, username=username, password_salt=password_salt, password_hash=password_hash)

	print user.pk
	print user.username
	print user.password_hash

	return SuccessResponse({
		'id': user.id,
		'token': get_token(user)
	})
