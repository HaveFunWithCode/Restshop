from django.urls import path
from .views import RegisterView, LoginAPIView, logoutView, ProfileView,AddressViewSet,verifyemail
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

routers=DefaultRouter()
routers.register('profile/address', AddressViewSet,basename='address')

urlpatterns = [

    path('register/',RegisterView.as_view(),name="register_user"),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('login/',LoginAPIView.as_view(),name='login'),
    path('logout/',logoutView.as_view(),name='logout'),
    path('profile/',ProfileView.as_view(),name='profile'),
    path('verify/(?P<uuid>[a-z0-9\-]+)/',verifyemail,name='verify'),
    # path('profile/orders',ProfileView.as_view(),name='orders'),

]
urlpatterns+=routers.urls