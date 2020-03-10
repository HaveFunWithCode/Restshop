from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from cart.cart import Cart


class CartView(APIView):
    permission_classes = [AllowAny]

    # show cart
    def get(self, request):
        # get cart content from database if exist
        pass

    # add to cart
    def post(self,request,product_unit_id,quantity=None):


        pass
