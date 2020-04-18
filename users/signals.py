from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from .tasks import send_verification_email

from .models import CustomerProfile
from .models import ShopUser
from cart.models import ShoppingCart
from datetime import datetime, timedelta



@receiver(post_save, sender=ShopUser)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        if not instance.is_superuser:
            CustomerProfile.objects.create(user=instance)
            ShoppingCart.objects.create(customer=instance).save()

            if not instance.is_verified:
                _20secondlater= datetime.utcnow() + timedelta(seconds=20)
                send_verification_email.apply_async((instance.pk,),eta=_20secondlater)
        # instance.customerProfile.save()

