from django.urls import path
from payment.views import PaymentView

urlpatterns = [
    path('<int:orderid>',PaymentView.as_view(),name='payment'),

]