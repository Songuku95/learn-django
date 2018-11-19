import datetime
import random
import string

# import bcrypt
import jwt
import hashlib


from enums import UserRoleName

# NOTE: Max password length is 72
PASSWORD_PEPPER = 'ZF[blc)j@z2%-c!c<(NCz.<:gn7o$S'
JWT_SECRET_KEY = 'RtyT+>T}SxkF-^e];_RY"3eZ,Y/I.3;iC?(*)gprxMSe|'
SALT_LENGTH = 12


def generate_password_salt():
	return ''.join(random.choice(string.printable) for _ in range(SALT_LENGTH))


def generate_password_hash(password, password_salt):
	# return bcrypt.hashpw((PASSWORD_PEPPER + password_salt + password).encode('ascii', 'ignore'), bcrypt.gensalt())
	return hashlib.sha512(PASSWORD_PEPPER + password_salt + password).hexdigest()


def check_password(password, password_salt, password_hash):
	# return bcrypt.checkpw((PASSWORD_PEPPER + password_salt + password).encode('ascii', 'ignore'),
	#                       password_hash.encode('ascii', 'ignore'))
	return hashlib.sha512(PASSWORD_PEPPER + password_salt + password).hexdigest() == password_hash


def get_token(user):
	iat = datetime.datetime.utcnow()
	return jwt.encode({
		'sub': user.id,
		'aud': UserRoleName.get_list()[user.role],
		'iat': iat,
		'exp': iat + datetime.timedelta(days=30)
	}, JWT_SECRET_KEY)


def decode_token(token, role):
	try:
		payload = jwt.decode(token, JWT_SECRET_KEY, audience=role)
	except jwt.InvalidTokenError:
		return None
	return payload
