from django.contrib.postgres.fields import JSONField
from django.db import models
from users.models import ShopUser


class ShoppingCart(models.Model):
    customer=models.ForeignKey(ShopUser,null=False,on_delete=models.CASCADE,related_name='cart')
    cart_session=JSONField(null=True)

