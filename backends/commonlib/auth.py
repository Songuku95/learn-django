import base64
import datetime
import random
import string
from functools import wraps
from hashlib import sha512, md5

import jwt
from Crypto.Cipher import AES

from commonlib.constant import UserRoleName
from commonlib.errors import Unauthorized

PASSWORD_PEPPER = 'ZF[blc)j@z2%-c!c<(NCz.<:gn7o$S'
JWT_SECRET_KEY = 'RtyT+>T}SxkF-^e];_RY"3eZ,Y/I.3;iC?(*)gprxMSe|'
SALT_LENGTH = 12
VERIFY_CODE_LENGTH = 18

# sha_raw_salt_password = sha512(raw_password+password_salt).hexdigest()
# encrypted_password = AES(sha_raw_salt_password, sha512(password_salt + verify_code))


def generate_password_salt():
	return ''.join(random.choice(string.printable) for _ in range(SALT_LENGTH))


def get_token(user):
	iat = datetime.datetime.utcnow()
	return jwt.encode({
		'sub': user['id'],
		'aud': UserRoleName.get_list()[user['role']],
		'iat': iat,
		'exp': iat + datetime.timedelta(days=30)
	}, JWT_SECRET_KEY)


def decode_token(token, role):
	try:
		payload = jwt.decode(token, JWT_SECRET_KEY, audience=role)
	except jwt.InvalidTokenError:
		return None
	return payload


def generate_verify_code():
	return ''.join(random.choice(string.letters) for _ in range(VERIFY_CODE_LENGTH))


def get_password_hash(encrypted_password, password_salt, verify_code):
	encrypted_password = base64.b64decode(encrypted_password)
	decryption_suite = AES.new(md5(password_salt + verify_code).hexdigest())
	md5_raw_salt_password = decryption_suite.decrypt(encrypted_password)
	password_hash = sha512(md5_raw_salt_password + PASSWORD_PEPPER).hexdigest()
	return password_hash


def require_auth(role):
	def require_auth_decorator(f):
		@wraps(f)
		def wrapper_func(request, *args, **kwargs):
			token = request.META.get('HTTP_AUTHORIZATION')
			if not token:
				raise Unauthorized()

			# Admin can access API for member
			if role == UserRoleName.ADMIN:
				payload = decode_token(token, UserRoleName.ADMIN)
			elif role == UserRoleName.MEMBER:
				payload = decode_token(token, UserRoleName.ADMIN) or decode_token(token, UserRoleName.MEMBER)
			else:
				raise Unauthorized()

			if not payload:
				raise Unauthorized()

			user_id = payload.get('sub')
			if not user_id:
				raise Unauthorized()

			request.user_id = user_id
			return f(request, *args, **kwargs)

		return wrapper_func

	return require_auth_decorator
