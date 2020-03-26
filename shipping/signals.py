from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Order
from .tasks import send_shipping_changed_email


@receiver(post_save,sender=Order)
def send_shipping_status_changed(sender, instance, created, **kwargs):
    if not created:
        if instance.shipping_status == Order.SENT:
            send_shipping_changed_email.delay(instance.customer.id)
