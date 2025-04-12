from django.db import models


# Create your models here.


class Cobon(models.Model):
    name = models.CharField(max_length=100)
    Sale = models.IntegerField()
    Eyear = models.IntegerField()
    Emonth = models.IntegerField()
    Eday = models.IntegerField()
    active = models.BooleanField(default=True)


class Task(models.Model):
    name = models.CharField(max_length=255) #
    desc = models.CharField(max_length=7000) #
    idea = models.CharField(max_length=255)#
    email = models.CharField(max_length=600)#
    number = models.CharField(max_length=30)#
    Domain = models.BooleanField(default=False)#
    Dynamic = models.BooleanField(default=False)#
    DB = models.BooleanField(default=False)#
    cobon = models.CharField(max_length=25)#
    price = models.FloatField()
    Date = models.CharField(max_length=255)
    Done = models.BooleanField(default=False)


