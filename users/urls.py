from django.urls import path, re_path
from .views import RegisterView, LoginAPIView, logoutView, ProfileView,AddressViewSet,verifyemail
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView





routers=DefaultRouter()
routers.register('profile/address', AddressViewSet,basename='address')

urlpatterns = [

    path('register/',RegisterView.as_view(),name="register_user"),
    path('login/',TokenObtainPairView.as_view(),name='login'),
    path('logout/',logoutView.as_view(),name='logout'),
    path('profile/',ProfileView.as_view(),name='profile'),
    re_path('^verify/(?P<uuid>[a-z0-9\-]+)/',verifyemail,name='verify'),
    # path('profile/orders',ProfileView.as_view(),name='orders'),
]
urlpatterns+=routers.urls