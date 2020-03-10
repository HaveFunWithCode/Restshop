from django.contrib.sessions.models import Session
from django.db import models
from users.models import ShopUser


class ShoppingCart(models.Model):
    customer=models.ForeignKey(ShopUser,null=False,on_delete=models.CASCADE,related_name='cart')
    cart_session=models.ForeignKey(Session,null=True,on_delete=models.CASCADE,related_name='cart')

