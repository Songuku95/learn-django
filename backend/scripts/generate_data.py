import random
import string

from enums import CommonStatus
from enums import UserRole
from events.models import CommentTab
from events.models import EventLikerTab
from events.models import EventTab, EventParticipantTab
from events.models import ImageTab, TagTab, EventTagTab
from users.auth import generate_password_salt, generate_password_hash
from users.models import UserTab

NUMBER_OF_ROWS = 1000000


def generate_users():
	password = '123123123'
	password_salt = generate_password_salt()
	password_hash = generate_password_hash(password, password_salt)

	for i in range(1, NUMBER_OF_ROWS + 1):
		email = 'test' + str(i) + '@test.com'
		username = 'test_' + str(i)

		UserTab.objects.create(
			email=email,
			username=username,
			password_salt=password_salt,
			password_hash=password_hash,
			fullname='fullname' + str(i),
			sex=i % 2,
			avatar_path='avatar' + str(i),
			role=UserRole.ADMIN
		)

		if i % 10000 == 0:
			print 'generate_users ' + str(i)


def generate_events():
	for i in range(1, NUMBER_OF_ROWS + 1):
		user_id = random.randint(1, NUMBER_OF_ROWS)
		EventTab.objects.create(
			title='title' + str(i),
			description='description' + str(i),
			start_date=0,
			end_date=0,
			address='address' + str(i),
			latitude=0,
			longitude=0,
			user_id=user_id,
		)

		if i % 10000 == 0:
			print 'generate_events ' + str(i)


def generate_images():
	for i in range(1, NUMBER_OF_ROWS + 1):
		ImageTab.objects.create(
			path='image' + str(i),
			event_id=random.randint(1, NUMBER_OF_ROWS)
		)
		if i % 10000 == 0:
			print 'generate_images ' + str(i)


def generate_comments():
	for i in range(1, NUMBER_OF_ROWS + 1):
		CommentTab.objects.get_or_create(
			event_id=random.randint(1, NUMBER_OF_ROWS),
			user_id=random.randint(1, NUMBER_OF_ROWS),
			content='content' + str(i)
		)
		if i % 10000 == 0:
			print 'generate_comments ' + str(i)


def generate_event_likers():
	for i in range(1, NUMBER_OF_ROWS + 1):
		EventLikerTab.objects.get_or_create(
			event_id=random.randint(1, NUMBER_OF_ROWS),
			user_id=random.randint(1, NUMBER_OF_ROWS),
			status=CommonStatus.ACTIVE
		)
		if i % 10000 == 0:
			print 'generate_event_likers ' + str(i)


def generate_event_participants():
	for i in range(1, NUMBER_OF_ROWS + 1):
		EventParticipantTab.objects.get_or_create(
			event_id=random.randint(1, NUMBER_OF_ROWS),
			user_id=random.randint(1, NUMBER_OF_ROWS),
			status=CommonStatus.ACTIVE
		)
		if i % 10000 == 0:
			print 'generate_event_participants ' + str(i)


def generate_tags():
	for i in range(1, NUMBER_OF_ROWS + 1):
		TagTab.objects.get_or_create(
			name=''.join(random.choice(string.printable) for _ in range(6))
		)
		if i % 10000 == 0:
			print 'generate_tags ' + str(i)


def generate_event_tags():
	for i in range(1, NUMBER_OF_ROWS + 1):
		EventTagTab.objects.get_or_create(
			tag_id=random.randint(1, NUMBER_OF_ROWS),
			event_id=random.randint(1, NUMBER_OF_ROWS)
		)
		if i % 10000 == 0:
			print 'generate_event_tags ' + str(i)


def run():
	generate_users()
	generate_events()
	generate_images()
	generate_comments()
	generate_event_likers()
	generate_event_participants()
	generate_tags()
	generate_tags()
