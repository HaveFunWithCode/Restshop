from django.db import models
from content.models import ProductUnit
from shop import settings
from users.models import ShopUser, Adress
from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    PENDING = 'pending'
    CANCLED = 'canceled'
    UNSUCCESSFUL = 'unsuccessful'
    SUCCESSFUL = 'successful'
    SENT = 'sent'
    DELIVERED = 'delivered'

    SHIPPING_STATUS = [
        (PENDING, _('Waiting for paying')),
        (CANCLED, _('Cancled order')),
        (UNSUCCESSFUL, _('Unsuccessfull payment')),
        (SUCCESSFUL, _('Successful payment')),
        (SENT, _('Sent to Customer')),
        (DELIVERED, _('Delivered to custumer'))
    ]

    customer = models.ForeignKey(ShopUser, null=False, on_delete=models.CASCADE)
    address = models.ForeignKey(Adress, null=True, on_delete=models.PROTECT)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    shipping_status = models.CharField(
        max_length=21,
        choices=SHIPPING_STATUS,
        default=PENDING,
    )
    total_price = models.PositiveIntegerField(null=False)

    class Meta:
        ordering = ('-created_at',)


    def __str__(self):
        return 'order {}'.format(self.id)


class OrderItem(models.Model):
    """
    in this model order item details will be saved after order
    register to refer to the product later (if available)
    and save price, name, and main image of product to keep trace of
    order if product removed in future
    """

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitems')
    product_unit = models.ForeignKey(ProductUnit, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField()
    main_image_path = models.ImageField(upload_to=settings.ORDERIMAGE_PATH)
    product_name = models.CharField(max_length=255, null=False, blank=False)
    product_unit_price = models.PositiveIntegerField(null=False)
    seller = models.CharField(max_length=255, null=False)


    def __str__(self):
        return '{}\n{}'.format(self.product_name,
                               self.seller)
