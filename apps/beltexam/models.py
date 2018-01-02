
# Create your models here.
from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import re
import bcrypt
import datetime
EMAILisnotvalid = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
passd = re.compile(r'^([^0-9]*|[^A-Z]*)$')
NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')
# Create your models here.

class LoginManager(models.Manager):

    def validate_login(self, postData):
        errors = []
        # check DB for post_data['email']
        if len(self.filter(username=postData['username'])) > 0:
            # check this user's password
            user = self.filter(username=postData['username'])[0]
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                errors.append('username/password incorrect')
        else:
            errors.append('username/password incorrect')

        if errors:
            return errors
        return user

    def validate_registration(self, postData):
        errors = []
        if len(postData['name']) < 3:
            errors.append("Name should be more than 3 characters")
        if len(postData['username'])< 3 :
            errors.append('username must be at least 3 characters')
        if len(postData['password']) < 8 :
            errors.append("Password should be more than 8 characters")
        if passd.match(postData['password']):
            errors.append("least 1 uppercase letter and 1 numeric value")
        if postData['password'] != postData['password_confirm']:
            errors.append("Password and Password Confirmation are not same")
        
        if not errors:
# make our new user
# hash password
            hashed = bcrypt.hashpw((postData['password'].encode()), bcrypt.gensalt(5))

            new_user = self.create(
                name=postData['name'],
                username=postData['username'],
                password=hashed
            )
            return new_user

        return errors

# class IManager(models.Manager):
#     def validate_add(self, postData):
#         errors = []
#         if len(postData['item']) < 3:
#             errors.append( )
#         if len(postData['item']) == 0:
#             errors.append("item entry should not be empty")
#         return errors

class User(models.Model):
    username = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = LoginManager()
    def __str__(self):
        return self.username

class Destination(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    startdate = models.DateTimeField(blank=True, default='', null=True)
    enddate = models.DateTimeField(blank=True, default='', null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    added = models.ForeignKey(User, related_name="added_destination")
    join_by = models.ManyToManyField(User, related_name="join_destination")
    # def clean_startdate(self):
    #     startdate = self.cleaned_data['startdate']
    #     if startdate < datetime.date.today():
    #         raise forms.ValidationError("The date cannot be in the past!")
    #     return startdate
    # objects = IManager()