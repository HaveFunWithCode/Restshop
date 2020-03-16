from rest_framework.serializers import ModelSerializer, JSONField, HyperlinkedModelSerializer, ListSerializer
from rest_framework import serializers
from .models import Product, ProductUnit


class ProductUnitSerializer(ModelSerializer):
    seller=serializers.ReadOnlyField(source='seller.name')

    class Meta:
        model=ProductUnit
        fields='__all__'

# product list with minimum specification
class ProductListSerializer(ModelSerializer):
    brand_name = serializers.ReadOnlyField(source='brand.brand_name')
    category_name = serializers.ReadOnlyField(source='category.category_name')
    main_image = serializers.SerializerMethodField()


    def get_main_image(self, obj):
        images = obj.images.order_by('is_default_pic')
        return [image.image_path.url for image in images][0]

    class Meta:
        model = Product
        fields = ('id', 'name', 'category','category_name', 'brand', 'brand_name', 'main_image')


class ProductDetaileSerializer(ModelSerializer):
    brand_name=serializers.ReadOnlyField(source='brand.brand_name')
    category_name=serializers.ReadOnlyField(source='category.category_name')
    product_units=serializers.SerializerMethodField()
    main_image=serializers.SerializerMethodField()

    def get_product_units(self,obj):
        product_uits=ProductUnit.objects.filter(product__id=obj.id)
        return ProductUnitSerializer(product_uits,
                                     many=True,
                                     read_only=True,
                                     context=self.context).data

    def get_main_image(self, obj):
        images = obj.images.order_by('is_default_pic')
        return [image.image_path.url for image in images][0]

    class Meta:
        model=Product
        fields=('id',
                'name',
                'description',
                'category',
                'category_name',
                'values',
                'brand',
                'brand_name',
                'main_image',
                'product_units')


# product list with maximum specification if needed
class ProductListDetailedSerializer(ListSerializer):
    brand_name=serializers.ReadOnlyField(source='brand.brand_name')
    category_name=serializers.ReadOnlyField(source='category.category_name')
    product_units=serializers.SerializerMethodField()
    main_image=serializers.SerializerMethodField()

    def get_product_units(self,obj):
        product_uits=ProductUnit.objects.filter(product__id=obj.id)
        return ProductUnitSerializer(product_uits,
                                     many=True,
                                     read_only=True,
                                     context=self.context).data

    def get_main_image(self, obj):
        images = obj.images.order_by('is_default_pic')
        return [image.image_path.url for image in images][0]

    class Meta:
        model=Product
        fields=('id','name','description','category',
                'category_name','values','brand','brand_name',
                'main_image','product_units')

