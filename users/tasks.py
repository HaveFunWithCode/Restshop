import logging
from celery import shared_task
from django.core.mail import send_mail
from django.urls import reverse

from users.models import ShopUser


@shared_task(name='send verification email')
def send_verification_email(user_id):

    try:
        user= ShopUser.objects.get(pk=user_id)
        send_mail(
            subject =' SepehrShop email verification',
            message =' Follow below link to verify your account: http://localhost:8007%s'% reverse('verify',kwargs={'uuid':str(user.verification_uuid)}),
            from_email = 'msshop202020@gmail.com',
            recipient_list=[user.email],
            fail_silently=False)

    except Exception as e:
        logging.warning('exp message '+str(e))

        # logging.warning("Tried to send verification email to non-existing user '%s'" % user_id)


