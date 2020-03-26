
from django.urls import path
from .views import add_category,get_brands
from rest_framework.routers import DefaultRouter
from .views import ProductListViewSet,CategoryListViewSet


routers=DefaultRouter()
routers.register('products',ProductListViewSet,basename='products')
routers.register('categories',CategoryListViewSet,basename='categories')




urlpatterns = [

    # path('add_category/',add_category,name='addcat'),
    path('add_category/',add_category.as_view(),name='addcat'),
    path('get_brands/',get_brands),

]
urlpatterns+=routers.urls
