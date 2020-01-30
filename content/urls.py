
from django.urls import path
from .views import add_category,get_brands

urlpatterns = [

    path('add_category/',add_category,name='addcat'),
    path('get_brands/',get_brands),

]
