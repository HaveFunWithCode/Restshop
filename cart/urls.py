from django.urls import path
from .views import CartView

urlpatterns=[
    path('',CartView.as_view(),name='cart'),
    path('add/<int:product_unit_id>/',CartView.as_view(),name='cartadd'),
    path('add/<int:product_unit_id>/<int:quantity>',CartView.as_view(),name='cartadd'),

    path('remove/<int:product_unit_id>/',CartView.as_view(),name='cartremove'),
    path('remove/<int:product_unit_id>/<int:quantity>',CartView.as_view(),name='cartremove'),

]