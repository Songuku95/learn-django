# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.db import models

from core import Model
from enums import CommonStatus


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
