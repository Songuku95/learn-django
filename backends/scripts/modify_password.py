from hashlib import sha512, md5
from Crypto.Cipher import AES
import base64

from commonlib import auth
from commonlib.models import UserTab


def run():
	password_salt = "fZ}hD'V$o}.H"
	raw_password = '123123123'
	md5_raw_salt_password = md5(raw_password + password_salt).hexdigest()
	password_hash = sha512(md5_raw_salt_password + auth.PASSWORD_PEPPER).hexdigest()

	# verify_code = 'dllDnoIULNXQhZJhMh'
	# encryption_suite = AES.new(md5(password_salt + verify_code).hexdigest())
	# print base64.b64encode(encryption_suite.encrypt(md5_raw_salt_password))
	# print md5_raw_salt_password
	# print password_hash

	for i in range(1, 1000):
		user = UserTab.objects.get(id=i)
		user.password_salt = password_salt
		user.password_hash = password_hash
		user.save()
