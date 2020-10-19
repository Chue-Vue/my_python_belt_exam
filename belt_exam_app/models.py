from django.db import models
import re

# Create your models here.

class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name']) < 3:
            errors['first_name'] = "First name must be longer than 3 characters"
        if len(postData['last_name']) < 3:
            errors['last_name'] = "Last name must be longer than 3 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email"
        if len(postData['password']) < 6:
            errors['password'] = "Password must be longer than 6 character"
        if postData['password'] != postData['confirm']:
            errors['confirm'] = "Passwords do not match!"
        return errors

    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['login_email']):
            errors['login_email'] = "Invalid email!"
        if len(postData['login_password']) < 6:
            errors['login_password'] = "Invalid  password!"
        return errors

    def edit_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['edit_email']):
            errors['edit_email'] = "Invalid email!"
        if len(postData['edit_first_name']) < 3:
            errors['edit_first_name'] = "First name must be longer than 3 characters"
        if len(postData['edit_last_name']) < 3:
            errors['edit_last_name'] = "Last name must be longer than 3 characters"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class AuthorManager(models.Manager):
    def author_validator(self, postData):
        errors = {}
        if len(postData['author']) < 3:
            errors['author'] = "Author must be longer than 3 characters"
        if len(postData['quote']) < 10:
            errors['quote'] = "Quote must be longer than 10 characters"
        return errors

class Author(models.Model):
    author = models.CharField(max_length=45)
    quote = models.TextField()
    user = models.ForeignKey(User, related_name ="authors", on_delete= models.CASCADE)
    likes = models.ManyToManyField(User, related_name="liked_by")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AuthorManager()
