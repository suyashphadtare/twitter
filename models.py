from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Token(models.Model):
    oauth_token = models.CharField(max_length=150)
    oauth_secret = models.CharField(max_length=150)
    user_id = models.CharField(max_length=100, default="Test1005")
