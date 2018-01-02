from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    first_name= models.CharField(max_length=101)
    last_name= models.CharField(max_length=101)
    email= models.CharField(max_length=101, unique=True)
    password= models.CharField(max_length=101)
    created_at= models.DateField(auto_now_add=True)
    updated_at= models.DateField(auto_now=True)

class Money(models.Model):
    income =  models.CharField(max_length=101)
    carPayment = models.CharField(max_length=101)
    newIncome = models.CharField(max_length=101)
    created_at= models.DateField(auto_now_add=True)
    updated_at= models.DateField(auto_now=True)


class Addition(models.Model):
    user= models.ForeignKey(User, related_name='additions')
    money = models.ForeignKey(Money, related_name='additions')
    created_at= models.DateField(auto_now_add=True)
    updated_at= models.DateField(auto_now=True)
