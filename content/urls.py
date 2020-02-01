
from django.urls import path
from .views import add_category,get_brands
from rest_framework.routers import SimpleRouter
from .views import ProductViewSet


routers=SimpleRouter()
routers.register('products',ProductViewSet,basename='products')


urlpatterns = [

    path('add_category/',add_category,name='addcat'),
    path('get_brands/',get_brands),


]
urlpatterns+=routers.urls
