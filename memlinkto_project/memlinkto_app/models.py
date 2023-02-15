from django.contrib.auth.models import User
from django.db import models
from allauth.account.models import EmailAddress


# Create your models here.

class UrlMapping(models.Model):
    email_address = models.ForeignKey(EmailAddress, on_delete=models.CASCADE)
    short_url = models.CharField(max_length=1000, db_index=True, unique=True)
    long_url = models.CharField(max_length=10000)
