import json

from django import forms
from django.contrib import admin
from django.forms import modelform_factory, modelformset_factory
from django_admin_json_editor import JSONEditorWidget
from entangled.forms import EntangledModelForm
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

class productUnitInline(admin.StackedInline):
    model = ProductUnit
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    list_display=('category_name','type')
    list_filter = ['type']


# TODO: add validation to product filed
# TODO: add variations to product filed
#
class ProductJSONModelAdminForm(forms.ModelForm):
    def __init__(self, *args,request=None, **kwargs):
        # load schema based on cat seleted
        if 'instance' in kwargs and kwargs['instance']!=None:
            cat_id=kwargs['instance'].category.id
        else:
            first_cat_row=Category.objects.values_list('id',flat=True).first()
            cat_id =  int(kwargs.get('initial')['catid']) if  'initial' in kwargs and 'catid' in kwargs.get('initial') else (int(args[0].get('category')) if len(args)>0 and 'category' in args[0] else first_cat_row)
        DATA_SCHEMA_name = Category.objects.values_list('attributes_Schema_name', flat=True).get(id=int(cat_id))
        with open("attSchemas/{0}".format(DATA_SCHEMA_name)) as jfile:
            DATA_SCHEMA = json.load(jfile)

        super().__init__(*args, **kwargs)


        self.initial['category']=cat_id
        self.fields['brand'].queryset=Brand.objects.filter(category_id=cat_id)

        # self.fields['values'].widget= JSONSchemaWidget(DATA_SCHEMA)

        self.fields['values'].widget= JSONEditorWidget(DATA_SCHEMA,False)



    class Meta:
        model = Product
        fields = "__all__"

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):

    list_display =['name','category']
    form = ProductJSONModelAdminForm
    inlines = [productUnitInline, productImageInline]
    fieldsets = [
        ('اطلاعات اصلی', {'fields': ['category', 'brand', 'name', 'values','description']}),

    ]
    change_form_template="content/my_product_admin.html"

    def save_model(self, request, obj, form, change):
        super(ProductModelAdmin, self).save_model(request, obj, form, change)

admin.site.register(Category,CategoryAdmin)
admin.site.register(Type)
admin.site.register(Brand)
admin.site.register(Supplier)
# admin.site.register(ProductUnit)