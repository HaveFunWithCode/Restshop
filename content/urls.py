
from django.urls import path
from .views import add_category,get_brands
from rest_framework.routers import DefaultRouter
from .views import ProductListViewSet


routers=DefaultRouter()
routers.register('products',ProductListViewSet,basename='products')



urlpatterns = [

    # path('add_category/',add_category,name='addcat'),
    path('add_category/',add_category.as_view(),name='addcat'),
    path('get_brands/',get_brands),

]
urlpatterns+=routers.urls
