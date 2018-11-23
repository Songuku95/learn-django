# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import time

from django.db import models

from commonlib.constant import CommonStatus, Sex, UserRole


# Reference: https://stackoverflow.com/questions/1737017/django-auto-now-and-auto-now-add
class Model(models.Model):
	created_at = models.PositiveIntegerField(editable=False)
	updated_at = models.PositiveIntegerField()

	def save(self, *args, **kwargs):
		# On saves, update timestamps
		now = int(time.time())
		if not self.id:
			self.created_at = now
		self.updated_at = now
		return super(Model, self).save(*args, **kwargs)

	class Meta:
		abstract = True


class UserTab(Model):
	username = models.CharField(max_length=20)
	fullname = models.CharField(max_length=20)
	sex = models.SmallIntegerField(default=Sex.PENDING)
	email = models.CharField(max_length=50)
	avatar_path = models.CharField(max_length=100)
	role = models.SmallIntegerField(default=UserRole.MEMBER)
	password_hash = models.CharField(max_length=100)
	password_salt = models.CharField(max_length=12)

	class Meta:
		db_table = 'user_tab'

	def __unicode__(self):
		return self.username


class EventTab(Model):
	user_id = models.PositiveIntegerField()
	title = models.CharField(max_length=200)
	description = models.CharField(max_length=10000)
	start_date = models.PositiveIntegerField()
	end_date = models.PositiveIntegerField()
	address = models.CharField(max_length=200)
	latitude = models.DecimalField(max_digits=11, decimal_places=8)
	longitude = models.DecimalField(max_digits=11, decimal_places=8)
	status = models.SmallIntegerField(default=CommonStatus.ACTIVE)

	class Meta:
		db_table = 'event_tab'

	def __unicode__(self):
		return self.title


class ImageTab(Model):
	path = models.CharField(max_length=100)
	event_id = models.PositiveIntegerField()
	status = models.SmallIntegerField(default=CommonStatus.ACTIVE)

	class Meta:
		indexes = [models.Index(fields=['event_id'], name='idx_event_id')]
		db_table = 'image_tab'

	def __unicode__(self):
		return self.path


class CommentTab(Model):
	event_id = models.PositiveIntegerField()
	user_id = models.PositiveIntegerField()
	content = models.CharField(max_length=10000)
	status = models.SmallIntegerField(default=CommonStatus.ACTIVE)

	class Meta:
		indexes = [models.Index(fields=['event_id'], name='idx_event_id')]
		db_table = 'comment_tab'

	def __unicode__(self):
		return self.content


class EventLikerTab(Model):
	user_id = models.PositiveIntegerField()
	event_id = models.PositiveIntegerField()
	status = models.SmallIntegerField(default=CommonStatus.ACTIVE)

	class Meta:
		indexes = [models.Index(fields=['event_id'], name='idx_event_id')]
		db_table = 'event_liker_tab'

	def __unicode__(self):
		return self.id


class EventParticipantTab(Model):
	user_id = models.PositiveIntegerField()
	event_id = models.PositiveIntegerField()
	status = models.SmallIntegerField(default=CommonStatus.ACTIVE)

	class Meta:
		indexes = [models.Index(fields=['event_id'], name='idx_event_id')]
		db_table = 'event_participant_tab'

	def __unicode__(self):
		return self.id


class TagTab(Model):
	name = models.CharField(max_length=20)
	idx_name = models.Index(fields=['name'])

	class Meta:
		indexes = [models.Index(fields=['name'], name='idx_name')]
		db_table = 'tag_tab'

	def __unicode__(self):
		return self.name


class EventTagTab(Model):
	tag_id = models.PositiveIntegerField()
	event_id = models.PositiveIntegerField()

	class Meta:
		indexes = [models.Index(fields=['tag_id'], name='idx_tag_id')]
		db_table = 'event_tag_tab'

	def __unicode__(self):
		return self.id
