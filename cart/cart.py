from decimal import Decimal

from django.conf import settings
from content.models import ProductUnit
from .models import ShoppingCart



class Cart(object):
    def __get_product_unit_count(self,pid):
        product_unit = ProductUnit.objects.all().filter(id=pid)
        if product_unit:
            # update price if exist from last session
            if str(pid) in self.session[settings.CART_SESSION_ID]:
                self.session[settings.CART_SESSION_ID][str(pid)]['price'] = product_unit[0].price
            return product_unit[0].storage_count
        else:
            # no such produt_unit_available
            return None


    def __check_product_availability(self,session_cart):

        self.availability_message={}
        for product_unit_id, attrs in session_cart.items():
            storage_count=self.__get_product_unit_count(product_unit_id)
            if storage_count is None or storage_count < attrs['quantity'] :
                self.availability_message[product_unit_id] = self.__get_product_unit_count(product_unit_id) or -1

            # product_unit=ProductUnit.objects.all().filter(id=product_unit_id)
            # if product_unit:
            #     if quantity>product_unit.storage_count:
            #         self.availability_message[product_unit_id]=product_unit.storage_count
            # else:
            #     # no such produt_unit_available
            #     self.availability_message[product_unit_id]=-1

    def __init__(self,request):
        # check is user authenticated or not
        if request.user.is_authenticated:
            # request db to get  abandoned items in last login
            last_login_cart_session=ShoppingCart.objests.all.filter(customer=request.user)
            if last_login_cart_session:
                last_session_cart=last_login_cart_session.get(settings.CART_SESSION_ID)


            new_session_cart=request.session.get(settings.CART_SESSION_ID)
            # merge two session with new added item (dupplicated item quantity will updated with new quantity)
            self.session=request.session
            self.session[settings.CART_SESSION_ID]={}
            for product_unit_id,quantity in new_session_cart.items():
                if product_unit_id in last_session_cart:
                    # update current session with new quantity
                    del last_session_cart[product_unit_id]
                    self.session[settings.CART_SESSION_ID][product_unit_id]=new_session_cart[product_unit_id]

            # check product availability &&
            # update number of item if not available anymore to zero( to show unavailability) or decrease to the highest possible number
            # TODO: this part of code MUST TEST with different situation
            self.__check_product_availability(self.session[settings.CART_SESSION_ID])
            if len(self.availability_message)>0:
                for puid,avilable_quantitly  in self.availability_message:
                    self.session[settings.CART_SESSION_ID][puid]['quantity'] = avilable_quantitly

            # add remained product in last_session_cart to current session
            # update request.session
            # TODO: this part of code MUST TEST with different situation
            request.session=self.cart=self.session[settings.CART_SESSION_ID]={**self.session[settings.CART_SESSION_ID] ,**last_login_cart_session }


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
        return sum(Decimal(cartItem['price']*cartItem['quantity']) for cartItem in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def add_to_cart(self, product_unit_id, quantity=1, update_quantity=False):
        self.availability_message = {}
        storage_count = self.__get_product_unit_count(product_unit_id)
        # if storage_count is None or storage_count < quantity:
        #     self.availability_message[product_unit_id] = self.__get_product_unit_count(product_unit_id) or -1
        # if this product_unit has no error
        if product_unit_id not in self.availability_message:


            if str(product_unit_id) not in self.cart:
                if storage_count is None or storage_count < quantity:
                    self.availability_message[product_unit_id] = self.__get_product_unit_count(product_unit_id) or -1
                else:
                    price = ProductUnit.objects.all().filter(id=product_unit_id)[0].price
                    self.cart[str(product_unit_id)]={'quantity':quantity,'price':price}
            if update_quantity:
                if storage_count is None or storage_count < quantity:
                    self.availability_message[product_unit_id] = self.__get_product_unit_count(product_unit_id) or -1
                else:
                    price = ProductUnit.objects.all().filter(id=product_unit_id)[0].price
                    self.cart[str(product_unit_id)]['quantity'] = quantity
                    self.cart[str(product_unit_id)]['price'] = price

            else:
                if storage_count is None or storage_count < quantity+self.cart[str(product_unit_id)]['quantity']:
                    self.availability_message[product_unit_id] = self.__get_product_unit_count(product_unit_id) or -1
                else:
                    price = ProductUnit.objects.all().filter(id=product_unit_id)[0].price
                    self.cart[str(product_unit_id)]['quantity']+=quantity
                    self.cart[str(product_unit_id)]['price']=price

            self.save()

    def remove_from_cart(self,product_unit):
        # TODO: check nmber of item you wanna remove |MUST MODIFY
        if str(product_unit.id) in self.cart:
            del self.cart[str(product_unit.id)]
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

