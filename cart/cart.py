from decimal import Decimal

from django.conf import settings
from content.models import ProductUnit

class Cart(object):
    def __init__(self,request):
        self.session=request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart=self.session[settings.CART_SESSION_ID]={}
        self.cart=cart

    def __len__(self):
        return sum(cartItem['quantity'] for cartItem in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(cartItem['price']*cartItem['quantity']) for cartItem in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def add_to_cart(self,product_unit,quantity=1,update_quantity=False):
        if product_unit.id not in self.cart:
            self.cart[product_unit.id]={'quantity':quantity}
        if update_quantity:
            self.cart[product_unit.id]['quantity']=quantity
        else:
            self.cart[product_unit.id]['quantity']+=quantity
        self.save()

    def remove_from_cart(self,prodcut_unit):
        if str(prodcut_unit.id) in self.cart:
            del prodcut_unit.id
            self.save()
    def save(self):
        self.session.modified = True


    # def __iter__(self):
    #     # add actual product to cart to show to us and calculate total price per product
    #     product_unit_ids = self.cart.keys()
    #     products=ProductUnit.objects.filter(id__in=product_unit_ids).\
    #         prefetch_related('id_product_unit_set')
    #     cart = self.cart.copy()
    #     # for product in products:
    #     #     cart[str(product.)]['product_unit']=product_unit.product
    #     #
    #     # for item in cart.values():

