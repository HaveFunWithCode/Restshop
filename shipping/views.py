from django.conf import settings
from django.core import serializers
from django.shortcuts import render, redirect
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ViewSet
from users.serializers import AddressSerializer

from users.models import Adress
from .serializers import  OrderSerializer

from cart.cart import Cart


class OrdersListView(ListAPIView):
    pass

class OrderView(APIView):

    permission_classes = [IsAuthenticated]


    def get(self, request):
        # check cart is empty got to cart page with message empty cart
        # else show total price and addresses to choose
        cart = Cart(request=request)
        if len(cart)> 0:
            total_price = cart.get_total_price()
            user = request.user
            adresses = Adress.objects.filter(user=user)
            addresses_data=AddressSerializer(adresses,many=True).data

            return Response({'addresses':addresses_data, 'totla price': total_price},content_type='application/json')

        else:
            # TODO: message should declare cart is empty
            return redirect('cart')

class OrederRegisterView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        # address_id = request.data['addressid']
        # total_parice = request.data['totalprice']
        serializer = OrderSerializer(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # if order registered go to payment page
        return  redirect('payment',orderid=serializer.instance.id)











