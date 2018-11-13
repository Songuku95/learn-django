import datetime
import random
import string

import bcrypt
import jwt

from configurations.settings import SECRET_KEY

SALT_LENGTH = 20


def generate_password_salt():
	return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(SALT_LENGTH))


def generate_password_hash(password, password_salt):
	return bcrypt.hashpw((SECRET_KEY + password_salt + password).encode('utf8'), bcrypt.gensalt())


def get_token(user):
	iat = datetime.datetime.utcnow()
	return jwt.encode({
		'sub': user.id,
		'aud': user.role,
		'iat': iat,
		'exp': iat + datetime.timedelta(days=30)
	}, SECRET_KEY)


def decode_token(token, role):
	try:
		payload = jwt.decode(token, SECRET_KEY, leeway=10, audience=role)
	except jwt.InvalidTokenError:
		return None
	return payload
