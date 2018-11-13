# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class UserTab(models.Model):
	id = models.PositiveIntegerField(primary_key=True)
	created_at = models.PositiveIntegerField()
	updated_at = models.PositiveIntegerField()
	username = models.CharField(max_length=20)
	fullname = models.CharField(max_length=20)
	sex = models.SmallIntegerField()
	email = models.CharField(max_length=50)
	avatar_path = models.CharField(max_length=100)
	role = models.SmallIntegerField()
	password_hash = models.CharField(max_length=200)
	password_salt = models.CharField(max_length=200)
