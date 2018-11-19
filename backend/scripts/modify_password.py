from users.models import UserTab

from users.auth import generate_password_salt, generate_password_hash, get_token, check_password


def run():
	for i in range(1, 10000):
		password_salt = generate_password_salt()
		password_hash = generate_password_hash('123123123', password_salt)
		user = UserTab.objects.get(id=i)
		user.password_salt = password_salt
		user.password_hash = password_hash
		user.save()
