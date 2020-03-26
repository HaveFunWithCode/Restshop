from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import SearchView, ProductListBasedOnCatViewSet

routers=DefaultRouter()
routers.register('<int:catid>/(?P<match>.+)/$',ProductListBasedOnCatViewSet,basename='advancesearch')
# routers.register('<int:catid>/',ProductListBasedOnCatViewSet,basename='advancesearch')
urlpatterns = [

    path('<int:catid>/',SearchView.as_view(),name='search'),


]
urlpatterns+=routers.urls