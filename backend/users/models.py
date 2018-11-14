# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from core import Model
from enums import UserRole, Sex


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
