from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Customer(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)


class Supplier(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=255,null=False,blank=False)
    def __str__(self):
        return self.name
