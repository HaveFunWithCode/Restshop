from django.contrib.auth.models import User
from django.urls import reverse

from .models import ShopUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail

from .models import CustomerProfile


@receiver(post_save, sender=ShopUser)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        if not instance.is_superuser:
            CustomerProfile.objects.create(user=instance)
            Token.objects.create(user=instance)
            if not instance.is_verified:
                send_mail(
                    'Verify your Shop account',
                    'Follow this link to verify your account: '
                    'http://localhost:8007%s' % reverse('verify', kwargs={'uuid': str(instance.verification_uuid)}),
                    'from@quickpublisher.dev',
                    [instance.email],
                    fail_silently=False,
                )


        instance.customerProfile.save()