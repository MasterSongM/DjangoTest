from django.db import models


# Create your models here.
# class User(models.Model):
#     userName = models.CharField(max_length=20)
#     passwd = models.CharField(max_length=25)
#     level = models.IntegerFieldField()


class Test(models.Model):
    name = models.CharField(max_length=20)
