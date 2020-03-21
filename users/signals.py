from django.contrib.auth.models import User
from .models import ShopUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from .models import CustomerProfile


@receiver(post_save, sender=ShopUser)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        if not instance.is_superuser:
            CustomerProfile.objects.create(user=instance)
            Token.objects.create(user=instance)
        instance.customerProfile.save()