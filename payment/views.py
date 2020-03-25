from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from shipping.models import Order


class PaymentView(APIView):

    def get(self,request,orderid):

        # payment_result=0
        # assume payment result is ok
        payment_result=1
        order = Order.objects.get(id=orderid)
        if payment_result:
            order.shipping_status =Order.SUCCESSFUL
            order.save(update_fields=['shipping_status'])
            return Response({'status':'successfull payed'})
        else:
            order.shipping_status = Order.UNSUCCESSFUL
            order.save(update_fields=['shipping_status'])
            return Response({'status': 'successfull payed'})
