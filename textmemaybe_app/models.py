from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django import forms

import datetime
import os

class Base(models.Model):
    created_at  = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now=True, auto_now_add=True)

    class Meta:
        abstract = True

class Number(Base):
    user = models.ForeignKey(User)
    number = models.IntegerField()
    name = models.CharField(blank=True, null=True, max_length=255)
    message = models.CharField(blank=True, null=True, max_length=255)
    sms_url = models.URLField(blank=True, null=True)

#     def __unicode__(self):