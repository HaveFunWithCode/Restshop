from django.urls import path
from shipping.views import OrderView, OrederRegisterView

urlpatterns = [
    path('',OrderView.as_view(),name='order'),
    path('register/',OrederRegisterView.as_view(),name='orderregister'),
]