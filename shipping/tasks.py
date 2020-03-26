import logging

from celery import shared_task
from django.core.mail import send_mail

from users.models import ShopUser


@shared_task(name='send shipping status')
def send_shipping_changed_email(user_id):
    try:
        user = ShopUser.objects.get(pk=user_id)
        send_mail(
            subject =' SepehrShop order status changed ',
            message =' Dear customer ,\n your order is approved by supplier and sent to your address.\n '
                     'Thank you for using online shops and staying at home:)',
            from_email = 'msshop202020@gmail.com',
            recipient_list=[user.email],
            fail_silently=False)


    except Exception as ex:
        logging.warning('exp message ' + str(ex))
