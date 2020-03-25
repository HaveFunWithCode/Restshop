from decimal import Decimal

from django.conf import settings
from content.models import ProductUnit
from .models import ShoppingCart
from collections import defaultdict



# TODO: show name of product in shopping cart
class Cart(object):

    def __get_product_unit_count(self, pid):
        product_unit = ProductUnit.objects.all().filter(id=pid)

        if product_unit:
            # update price if exist from last session
            if self.session[settings.CART_SESSION_ID] and str(pid) in self.session[settings.CART_SESSION_ID]:
                self.session[settings.CART_SESSION_ID][str(pid)]['price'] = product_unit[0].price
            return product_unit[0].storage_count
        return None

    def __check_product_availability(self, session_cart):

        self.availability_message = {}
        if session_cart:
            for product_unit_id, attrs in session_cart.items():
                storage_count = self.__get_product_unit_count(product_unit_id)
                if storage_count is None or storage_count < attrs['quantity']:
                    self.availability_message[product_unit_id] = self.__get_product_unit_count(product_unit_id) or -1

    def __init__(self, request):

        self.request = request
        # check is user authenticated or not
        if request.user.is_authenticated:
            # request db to get  abandoned items in last login
            last_login_cart_session = ShoppingCart.objects.get(customer=request.user)
            last_session_cart = last_login_cart_session.cart_session if last_login_cart_session else {}
            new_session_cart = request.session.get(settings.CART_SESSION_ID) or {}

            # merge two session with new added item (dupplicated item quantity will updated with new quantity)
            self.session = request.session
            # self.session[settings.CART_SESSION_ID]= {}
            if new_session_cart:
                for product_unit_id, attrs in new_session_cart.items():
                    if last_session_cart and product_unit_id in last_session_cart:
                        # update current session with new quantity
                        del last_session_cart[product_unit_id]
                        self.session[settings.CART_SESSION_ID][product_unit_id] = new_session_cart[product_unit_id]

                # add remained not repeated element to cart
                if last_session_cart:
                    self.session[settings.CART_SESSION_ID].update(last_session_cart)
                if new_session_cart:
                    self.session[settings.CART_SESSION_ID].update(new_session_cart)


            else:
                self.session[settings.CART_SESSION_ID] = last_session_cart

            # check product availability &&
            # update number of item if not available anymore to zero( to show unavailability) or decrease to the highest possible number
            # TODO: this part of code MUST TEST with different situation
            self.__check_product_availability(self.session[settings.CART_SESSION_ID])
            if len(self.availability_message) > 0:
                for puid, avilable_quantitly in self.availability_message.items():
                    self.session[settings.CART_SESSION_ID][puid]['quantity'] = avilable_quantitly

            # add remained product in last_session_cart to current session
            # update request.session
            # TODO: this part of code MUST TEST with different situation
            request.session = self.cart = self.session[settings.CART_SESSION_ID] or {}

        else:
            self.session = request.session

            cart = self.session.get(settings.CART_SESSION_ID)
            if not cart:
                cart = self.session[settings.CART_SESSION_ID] = {}
            else:
                # check product availability &&
                # update number of item if not available anymore to zero( to show unavailability) or decrease to the highest possible number
                # in  delayed shipping this check is needed
                self.__check_product_availability(self.session[settings.CART_SESSION_ID])
                if len(self.availability_message) > 0:
                    for puid, avilable_quantitly in self.availability_message.items():
                        self.session[settings.CART_SESSION_ID][puid]['quantity'] = avilable_quantitly
                    cart = self.session[settings.CART_SESSION_ID]

            self.cart = cart

    def __len__(self):
        return sum(cartItem['quantity'] for cartItem in self.cart.values())

    def get_total_price(self):
        if self.cart:
            return sum(Decimal(cartItem['price'] * cartItem['quantity']) for cartItem in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        del self.cart
        self.session.modified = True
        # self.save()

    def add_to_cart(self, product_unit_id, quantity=1, update_quantity=False):
        self.availability_message = {}
        storage_count = self.__get_product_unit_count(product_unit_id)
        if product_unit_id not in self.availability_message:

            if  self.cart and str(product_unit_id) not in self.cart:
                if storage_count is None or storage_count < quantity:
                    self.availability_message[product_unit_id] = self.__get_product_unit_count(product_unit_id) or -1
                else:
                    price = ProductUnit.objects.all().filter(id=product_unit_id)[0].price
                    self.cart[str(product_unit_id)] = {'quantity': quantity, 'price': price}
            if update_quantity:
                if storage_count is None or storage_count < quantity:
                    self.availability_message[product_unit_id] = self.__get_product_unit_count(product_unit_id) or -1
                else:
                    price = ProductUnit.objects.all().filter(id=product_unit_id)[0].price
                    self.cart[str(product_unit_id)]['quantity'] = quantity
                    self.cart[str(product_unit_id)]['price'] = price

            else:
                if storage_count is None or (str(product_unit_id) in self.cart
                                             and storage_count < quantity + self.cart[str(product_unit_id)]['quantity']):
                    self.availability_message[product_unit_id] = self.__get_product_unit_count(product_unit_id) or -1
                else:
                    price = ProductUnit.objects.all().filter(id=product_unit_id)[0].price
                    if str(product_unit_id) in self.cart:

                        self.cart[str(product_unit_id)]['quantity'] += quantity
                        self.cart[str(product_unit_id)]['price'] = price
                    else:
                        self.cart[str(product_unit_id)]={}
                        self.cart[str(product_unit_id)]['quantity'] = quantity
                        self.cart[str(product_unit_id)]['price'] = price



            self.save()

    def remove_from_cart(self, product_unit_id):

        if str(product_unit_id) in self.cart:
            if int(self.cart[str(product_unit_id)]['quantity']) > 1:
                self.cart[str(product_unit_id)]['quantity'] = int(self.cart[str(product_unit_id)]['quantity']) - 1
            else:
                del self.cart[str(product_unit_id)]
            self.save()

    def save(self):
        self.session.modified = True
        self.session= self.cart
        if self.request.user.is_authenticated:
            shopcart = ShoppingCart.objects.get_or_create(customer=self.request.user)[0]
            shopcart.cart_session = self.session[settings.CART_SESSION_ID]
            shopcart.save()



