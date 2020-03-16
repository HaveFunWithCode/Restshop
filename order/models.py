from  django.db import models

from users.models import ShopUser, Adress


class Order(models.Model):
    customer=models.ForeignKey(ShopUser,null=False,on_delete=models.CASCADE,related_name='cart')
    address=models.ForeignKey(Adress,null=True)