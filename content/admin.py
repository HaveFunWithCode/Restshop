import json

from django import forms
from django.contrib import admin
from django.contrib.postgres.forms import JSONField
from django.forms import modelform_factory
from django_admin_json_editor import JSONEditorWidget
from jsonschemaform.admin.widgets.jsonschema_widget import JSONSchemaWidget

from .models import Category, Product, Type, Brand, ProductUnit, Supplier, Image, JSONSchemaField


class productImageInline(admin.TabularInline):
    model = Image
    extra = 1
    verbose_name='افزودن تصاویر'
    verbose_name_plural='تصاویر محصول'
    fieldsets = [
        ('افزودن تصویر',{'fields':['image_path','is_default_pic'],'classes': ['collapse']})
    ]

class productUnitInline(admin.TabularInline):
    model = ProductUnit
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    # fields = ['name','description','seller','category']
    fieldsets = [
        ('اطلاعات اصلی',{'fields':['name','description','category','brand']}),
        ('ویژگی های هر محصول',{'fields':['values']}),
    ]
    inlines = [productUnitInline,productImageInline]


class CategoryAdmin(admin.ModelAdmin):
    list_display=('category_name','type')
    list_filter = ['type']



#
#
# DATA_SCHEMA = {"$schema": "http://json-schema.org/schema#", "type": "object", "properties": {"cpu": {"type": "string"}, "ram": {"type": "string"}, "usb \u062f\u0627\u0631\u062f": {"type": "boolean"}}}
# class ProductJSONModelAdminForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields="__all__"
#         widgets = {
#             'values': JSONEditorWidget(DATA_SCHEMA, collapsed=False),
#         }

def Make_ProductJSONModelAdminForm():
    class ProductJSONModelAdminForm(forms.ModelForm):
        def __init__(self, *args,request=None, **kwargs):

            cat_id =  int(kwargs.get('initial')['id']) if 'id' in kwargs.get('initial') else 1
            DATA_SCHEMA_name = Category.objects.values_list('attributes_Schema_name', flat=True).get(id=int(cat_id))
            with open("attSchemas/{0}".format(DATA_SCHEMA_name)) as jfile:
                DATA_SCHEMA = json.load(jfile)
            widgets = {
                'values': JSONEditorWidget(DATA_SCHEMA, collapsed=False),
            }

            super(ProductJSONModelAdminForm, self).__init__(*args, **kwargs)

            self._meta['values'].widget= JSONEditorWidget(DATA_SCHEMA)





        class Meta:
            model = Product
            fields = "__all__"

    return ProductJSONModelAdminForm
class ProductJSONModelAdminForm(forms.ModelForm):
    def __init__(self, *args,request=None, **kwargs):

        cat_id =  int(kwargs.get('initial')['id']) if 'id' in kwargs.get('initial') else 1
        DATA_SCHEMA_name = Category.objects.values_list('attributes_Schema_name', flat=True).get(id=int(cat_id))
        with open("attSchemas/{0}".format(DATA_SCHEMA_name)) as jfile:
            DATA_SCHEMA = json.load(jfile)

        super().__init__(*args, **kwargs)

        self.fields['values'].widget= JSONEditorWidget(DATA_SCHEMA)


    class Meta:
        model = Product
        fields = "__all__"
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):

    form = ProductJSONModelAdminForm
    inlines = [productUnitInline, productImageInline]

# @admin.register(Product)
# class ProductModelAdmin(admin.ModelAdmin):
#     # form = ProductJSONModelAdminForm
#
#     # fieldsets = [
#     #     ('اطلاعات اصلی', {'fields': ['name', 'description', 'category', 'brand']}),
#     #     ('ویژگی های هر محصول', {'fields': ['values']}),
#     # ]
#     # inlines = [productUnitInline, productImageInline]
#
#     def get_form(self, request, obj=None, change=False, **kwargs):
#         catid = request.GET.get('id', 1)
#
#         DATA_SCHEMA_name = Category.objects.values_list('attributes_Schema_name', flat=True).get(id=int(catid))
#         with open("attSchemas/{0}".format(DATA_SCHEMA_name)) as jfile:
#             DATA_SCHEMA = json.load(jfile)
#         #
#         # # form = Make_ProductJSONModelAdminForm(cat_id=id)
#         # form = super().get_form(request,
#         #                         obj,
#         #                         widgets={
#         #                             'values': JSONEditorWidget(DATA_SCHEMA, collapsed=False),
#         #                         })
#         #                         # widgets={'tags': widget}, **kwargs)
#         # def dynamic_schema(widget):
#         #
#         #     DATA_SCHEMA_name = Category.objects.values_list('attributes_Schema_name', flat=True).get(id=int(catid))
#         #     with open("attSchemas/{0}".format(DATA_SCHEMA_name)) as jfile:
#         #         DATA_SCHEMA = json.load(jfile)
#         #         return DATA_SCHEMA
#
#
#
#         form = super().get_form(request, obj,
#                                 widgets={
#                                     'values': JSONEditorWidget(DATA_SCHEMA, collapsed=False),
#                                 }
#                                 , **kwargs)
#         # kwargs['form'] = form
#         return super().get_form(request, obj, **kwargs)
#     def change_view(self, request, object_id, form_url='', extra_context=None):
#         pass

# @admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):

    def get_form(self, request, obj=None, change=False, **kwargs):
        # catid = request.GET.get('id', 1)
        # DATA_SCHEMA_name = Category.objects.values_list('attributes_Schema_name', flat=True).get(id=int(catid))
        # with open("attSchemas/{0}".format(DATA_SCHEMA_name)) as jfile:
        #     DATA_SCHEMA = json.load(jfile)
        # form = super().get_form(request, obj,
        #                         widgets={
        #                             'values': JSONEditorWidget(DATA_SCHEMA, collapsed=False),
        #                         }
        #                         , **kwargs)
        # # kwargs['form'] = form
        catid = request.GET.get('id', 1)
        DATA_SCHEMA_name = Category.objects.values_list('attributes_Schema_name', flat=True).get(id=int(catid))
        with open("attSchemas/{0}".format(DATA_SCHEMA_name)) as jfile:
            DATA_SCHEMA = json.load(jfile)
        widget = JSONEditorWidget(DATA_SCHEMA, collapsed=False)


        form = modelform_factory(Product, widgets={'values': widget},fields="__all__")
        return form

    inlines = [productUnitInline, productImageInline]



admin.site.register(Category,CategoryAdmin)
admin.site.register(Type)
admin.site.register(Brand)
admin.site.register(Supplier)
admin.site.register(ProductUnit)