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

class Employee(models.Model):
    First_name = models.CharField(max_length=255)
    Last_name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    salary = models.CharField(max_length=30)
    about = models.CharField(max_length=99999)
    email = models.CharField(max_length=600)#
    number = models.CharField(max_length=30)#
    job = models.CharField(max_length=255)
    cv = models.FileField()
    prto = models.CharField(max_length=255)
    
    Eyear = models.IntegerField()
    Emonth = models.IntegerField()
    Eday = models.IntegerField()
    Syear = models.IntegerField()
    Smonth = models.IntegerField()
    Sday = models.IntegerField()
    active = models.BooleanField(default=True)
    def __str__(self):
        return f'{self.job}: {self.First_name} {self.Last_name} '


class Jobs(models.Model):
    name = models.CharField(max_length=255)



