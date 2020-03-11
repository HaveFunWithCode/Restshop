from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.cart import Cart


class CartView(APIView):
    permission_classes = [AllowAny]

    # show cart
    def get(self, request,):
        # get cart content from database if exist
        requestCart=Cart(request=request)
        # TODO: test current request test is changes or not
        return Response({'cart':requestCart.cart,'messages': getattr(requestCart,'availability_message',''),'total_price':requestCart.get_total_price()})

    # add to cart
    def post(self,request,product_unit_id,quantity=None):
        # check product unit availability if not return error or exeption
        requestCart = Cart(request=request)
        requestCart.add_to_cart(product_unit_id,quantity or 1)
        return Response({'cart': requestCart.cart, 'messages': getattr(requestCart,'availability_message',''),'total_price':requestCart.get_total_price()})

    def delete(self,request,product_unit_id):
        requestCart = Cart(request=request)
        requestCart.remove_from_cart(product_unit_id)
        return Response({'cart' :requestCart.cart, 'messages': getattr(requestCart,'availability_message',''),'total_price':requestCart.get_total_price()})



