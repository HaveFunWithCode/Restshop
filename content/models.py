import json
import os

from django.db import models
from users.models import SupplierUser
from django.conf import settings
from django.utils import inspect
from jsonschema import validate, exceptions as jsonschema_exceptions
from django.core import exceptions
from django.contrib.postgres.fields import JSONField
from django.utils import timezone

class JSONSchemaField(JSONField):
    """ https://gist.githubusercontent.com/saadullahaleem/78603764a19441467e7988c9e5ed8bdf/raw/6bb95f5a531b515fb6a3c9c52933009d4ffe803b/jsonschemafield.py """

    def __init__(self, *args, **kwargs):
        self.schema = kwargs.pop('schema', None)
        super().__init__(*args, **kwargs)

    @property
    def _schema_data(self):
        model_file = inspect.getfile(self.model)
        dirname = os.path.dirname(model_file)
        # schema file related to model.py path
        p = os.path.join(dirname, self.schema)
        with open(p, 'r') as file:
            return json.loads(file.read())

    def _validate_schema(self, value):

        # Disable validation when migrations are faked
        if self.model.__module__ == '__fake__':
            return True
        try:
            status = validate(value, self._schema_data)
        except jsonschema_exceptions.ValidationError as e:
            raise exceptions.ValidationError(e.message, code='invalid')
        return status

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        self._validate_schema(value)

    def pre_save(self, model_instance, add):
        value = super().pre_save(model_instance, add)
        if value and not self.null:
            self._validate_schema(value)
        return value

class Type(models.Model):
    type_name=models.CharField(max_length=255,null=True,unique=True)
    parrentType=models.ForeignKey("self",null=True,blank=True,on_delete=models.CASCADE)
    def __str__(self):
        return self.type_name



class Category(models.Model):
    category_name=models.CharField(max_length=255,unique=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    attributes_Schema_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name

class Brand(models.Model):
    category=models.ForeignKey(Category,null=False,related_name='brands',on_delete=models.CASCADE)
    brand_name=models.CharField(max_length=255,null=True)

    def __str__(self):
        return '({0}){1}'.format(self.category.category_name,self.brand_name)

class Product(models.Model):
    name=models.CharField(max_length=255,null=False,blank=False,verbose_name='نام محصول')
    description=models.TextField(max_length=10000,null=True,blank=True,verbose_name='توضیحات')
    category=models.ForeignKey(Category,null=False,verbose_name='دسته',on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)

    values = JSONField(verbose_name='ویژگی ها')
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE,null=True,verbose_name='برند')

    def __str__(self):

        return self.name
    class Meta:
        verbose_name=("محصول")
        verbose_name_plural=("محصولات")

class ProductUnit(models.Model):
    product = models.ForeignKey(Product,related_name='product_unit',on_delete=models.CASCADE)
    variant = JSONField(null=True)
    variant_title = models.CharField(max_length=255,null=True)
    seller = models.ForeignKey(SupplierUser,null=False,verbose_name='فروشنده',on_delete=models.CASCADE)
    price = models.PositiveIntegerField(null=False,verbose_name='قیمت')
    storage_count = models.PositiveIntegerField(null=False,verbose_name='تعداد در انبار این فروشگاه')

class Image(models.Model):

    product = models.ForeignKey(Product,related_name='images',on_delete=models.CASCADE)
    image_path = models.ImageField(upload_to=settings.PRODUCTIMAGE_PATH)
    is_default_pic = models.BooleanField(default=False)


