from rest_framework.serializers import ModelSerializer,JSONField
from . models import Product

class ProductSerializer(ModelSerializer):


    class Meta:
        model=Product
        fields=['id','name','description','category','values','brand']

