from django.db import models

# Create your models here.

class UserLogin(models.Model):
    email = models.CharField()
    password = models.CharField()
class UserRegestration(models.Model):
    email = models.CharField()
    password = models.CharField()
    nikname = models.CharField()