from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from content.views import add_category,get_brands
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('content/',include('content.urls')),
    path('',include('content.urls')),
    path('users/',include('users.urls')),
    path('cart/',include('cart.urls')),
    path('shipping/',include('shipping.urls')),
    path('payment/',include('payment.urls')),
    path('search/',include('search.urls')),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
