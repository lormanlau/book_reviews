# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
	def validate(self, user_data):
		errors = {}
		if len(user_data['name']) < 2:
			errors['name'] = "Name should be more than 2 letters long"
		if len(user_data['alias']) <2:
			errors['alias'] = "Alias should be more than 2 letters long"
		if not EMAIL_REGEX.match(user_data['email']):
			errors['email'] = "Invalid email address"
		if user_data['pass'] != user_data['con_pass']:
			errors['password'] = "Password does not match"
		return errors

# Create your models here.
class Books(models.Model):
	title = models.CharField(max_length=255)
	author = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)

class Users(models.Model):
	name = models.CharField(max_length=255)
	alias = models.CharField(max_length=255)
	email = models.EmailField()
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = UserManager()

class Reviews(models.Model):
	book = models.ForeignKey(Books)
	user = models.ForeignKey(Users)
	text = models.TextField()
	rating = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)