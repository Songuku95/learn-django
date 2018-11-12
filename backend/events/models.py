# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.db import models


class EventTab(models.Model):
	id = models.PositiveIntegerField(primary_key=True)
	created_at = models.PositiveIntegerField()
	updated_at = models.PositiveIntegerField()
	user_id = models.PositiveIntegerField()
	title = models.CharField(max_length=200)
	description = models.CharField(max_length=10000)
	start_date = models.PositiveIntegerField()
	end_date = models.PositiveIntegerField()
	location_name = models.CharField(max_length=200)
	location_x = models.DecimalField(max_digits=11, decimal_places=8)
	location_y = models.DecimalField(max_digits=11, decimal_places=8)
	status = models.SmallIntegerField()


class ImageTab(models.Model):
	id = models.PositiveIntegerField(primary_key=True)
	created_at = models.PositiveIntegerField()
	updated_at = models.PositiveIntegerField()
	path = models.CharField(max_length=100)
	event_id = models.PositiveIntegerField()
	status = models.SmallIntegerField()

	class Meta:
		indexes = [models.Index(fields=['event_id'], name='idx_event_id')]


class CommentTab(models.Model):
	id = models.PositiveIntegerField(primary_key=True)
	created_at = models.PositiveIntegerField()
	updated_at = models.PositiveIntegerField()
	event_id = models.PositiveIntegerField()
	user_id = models.PositiveIntegerField()
	content = models.CharField(max_length=10000)
	status = models.SmallIntegerField()

	class Meta:
		indexes = [models.Index(fields=['event_id'], name='idx_event_id')]


class EventLikerTab(models.Model):
	id = models.PositiveIntegerField(primary_key=True)
	created_at = models.PositiveIntegerField()
	updated_at = models.PositiveIntegerField()
	user_id = models.PositiveIntegerField()
	event_id = models.PositiveIntegerField()
	status = models.SmallIntegerField()

	class Meta:
		indexes = [models.Index(fields=['event_id'], name='idx_event_id')]


class EventParticipantTab(models.Model):
	id = models.PositiveIntegerField(primary_key=True)
	created_at = models.PositiveIntegerField()
	updated_at = models.PositiveIntegerField()
	user_id = models.PositiveIntegerField()
	event_id = models.PositiveIntegerField()
	status = models.CharField(max_length=10)

	class Meta:
		indexes = [models.Index(fields=['event_id'], name='idx_event_id')]


class TagTab(models.Model):
	id = models.PositiveIntegerField(primary_key=True)
	name = models.CharField(max_length=20)
	idx_name = models.Index(fields=['name'])


class EventTagTab(models.Model):
	id = models.PositiveIntegerField(primary_key=True)
	tag_id = models.PositiveIntegerField()
	event_id = models.PositiveIntegerField()

	class Meta:
		indexes = [models.Index(fields=['tag_id'], name='idx_tag_id')]
