import json

from django import forms
from django.contrib import admin
from django.forms import modelform_factory, modelformset_factory
from django_admin_json_editor import JSONEditorWidget
from entangled.forms import EntangledModelForm
from jsonschemaform.admin.widgets.jsonschema_widget import JSONSchemaWidget


from .models import Category, Product, Type, Brand, ProductUnit, Supplier, Image, JSONSchemaField


class productImageInline(admin.StackedInline):
    model = Image
    extra = 1
    verbose_name='افزودن تصاویر'
    verbose_name_plural='تصاویر محصول'
    fieldsets = [
        ('افزودن تصویر',{'fields':['image_path','is_default_pic'],'classes': ['collapse']})
    ]



class CategoryAdmin(admin.ModelAdmin):
    list_display=('category_name','type')
    list_filter = ['type']
#
# class productUnitJsonForm(forms.ModelForm):
#
#     class Meta:
#         model = ProductUnit
#         fields="__all__"


class VariantsWidget(forms.MultiWidget):

        def __init__(self,names,values,attrs=None):
            w=[]
            for i,name in enumerate(names):
                w.append(forms.Select(choices=tuple([(val,val) for val in values[i]])))

            widgets=tuple(w)
            super(VariantsWidget,self).__init__(widgets,attrs=attrs)

        def decompress(self, value):
            if value:
                val = value
                return val[:3],val[3:6],val[6:]
            return None,None,None

        def compress(self, data_list):
            if data_list[0] and data_list[1] and data_list[2]:
                return '%s''%s''%s' %(data_list[0],data_list[1],data_list[2])
            else:
                return None

        def value_from_datadict(self,data,files,name):
            val_list = [widget.value_from_datadict(data,files,name+'_%s' %i) for i,widget in enumerate(self.widgets)]
            if val_list:
                return '%s''%s''%s' %(val_list[0],val_list[1],val_list[2])

        def format_output(self,rendered_widgets):
            return '( '+rendered_widgets[0]+' )'+rendered_widgets[1]+' - '+rendered_widgets[2]
class productUnitJsonForm(forms.ModelForm):



    def __init__(self, *args, **kwargs):

        super(productUnitJsonForm,self).__init__(*args, **kwargs)
        DATA_SCHEMA = {
            'type': 'object',
            'title': 'Data',
            'properties': {

                'color': {
                    'title': 'color',
                    'type': 'string',
                    'enum': ['red', 'blue', 'black']
                },
                'size': {
                    'title': 'size',
                    'type': 'string',
                    'enum': ['L', 'M', 'S']
                }

            },
            "required": ['color','size']
        }

        # self.fields['variant'].widget =forms.MultiWidget(widgets=[forms.Select(choices=(('g','gg'),('dd','ddd'))),
        #                                                           forms.Select(choices=(('a','aa'),('b','bb')))])
        # self.fields['variant'].widget = forms.Select(choices=(('g','gg'),('dd','ddd')))
        # self.fields['variant'].widget = JSONEditorWidget(DATA_SCHEMA, False)
        self.fields['variant'].widget=VariantsWidget(['color','size'],[['red','black'],['L','M','S']])

    class Meta:
        model = ProductUnit
        fields="__all__"
#
#
#
#
#
#     # def __init__(self, *args,request=None, **kwargs):
#     #     # load schema based on cat seleted
#     #
#     #     # if 'instance' in kwargs and kwargs['instance']!=None:
#     #     #     cat_id=kwargs['instance'].category.id
#     #     # else:
#     #     #     first_cat_row=Category.objects.values_list('id',flat=True).first()
#     #     #     cat_id =  int(kwargs.get('initial')['catid']) if  'initial' in kwargs and 'catid' in kwargs.get('initial') else (int(args[0].get('category')) if len(args)>0 and 'category' in args[0] else first_cat_row)
#     #     # DATA_SCHEMA_name = Category.objects.values_list('attributes_Schema_name', flat=True).get(id=int(cat_id))
#     #     # with open("attSchemas/{0}".format(DATA_SCHEMA_name)) as jfile:
#     #     #     DATA_SCHEMA = json.load(jfile)
#     #
#     #     super().__init__(*args, **kwargs)
#     #     DATA_SCHEMA = {
#     #         'type': 'object',
#     #         'title': 'Data',
#     #         'properties': {
#     #             'text': {
#     #                 'title': "text",
#     #                 'type': 'string',
#     #                 'format': 'textarea',
#     #             },
#     #             'status': {
#     #                 'title': 'Status',
#     #                 'type': 'boolean',
#     #             },
#     #             'color': {
#     #                 'title': 'color',
#     #                 'type': 'string',
#     #                 'enum': ['red', 'blue', 'black']
#     #             },
#     #             'size': {
#     #                 'title': 'size',
#     #                 'type': 'string',
#     #                 'enum': ['L', 'M', 'S']
#     #             }
#     #
#     #         },
#     #         "required": ['color']
#     #     }
#     #     self.fields['variant'].widget = JSONEditorWidget(DATA_SCHEMA, True)
#     #
# @admin.register(ProductUnit)
# class productUnit(admin.ModelAdmin):
#     model = ProductUnit
#     form=productUnitJsonForm
#     extra = 1
#     fields =["variant","variant_title","seller","price","storage_count"]

class productUnitInline(admin.StackedInline):
    model = ProductUnit
    form=productUnitJsonForm
    extra = 1
    fields =["variant","variant_title","seller","price","storage_count"]




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

        DATA_SCHEMA = {
            'type': 'object',
            'title': 'Data',
            'properties': {
                'text': {
                    'title': "text",
                    'type': 'string',
                    'format': 'textarea',
                },
                'status': {
                    'title': 'Status',
                    'type': 'boolean',
                },
                'color': {
                    'title': 'color',
                    'type': 'string',
                    'enum':['red','blue','black']
                },
                'size':{
                    'title': 'size',
                    'type': 'string',
                    'enum': ['L', 'M', 'S']
                }

            },
            "required":['color']
        }


        self.fields['values'].widget= JSONEditorWidget(DATA_SCHEMA)

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

    # def get_formsets_with_inlines(self, request, obj=None):
    #     # for inline in self.get_inline_instances(request, obj):
    #     #     form = inline.form
    #     #
    #     #     DATA_SCHEMA = {
    #     #         'type': 'object',
    #     #         'title': 'Data',
    #     #         'properties': {
    #     #
    #     #             'color': {
    #     #                 'title': 'color',
    #     #                 'type': 'string',
    #     #                 'enum': ['red', 'blue', 'black']
    #     #             },
    #     #             'size': {
    #     #                 'title': 'size',
    #     #                 'type': 'string',
    #     #                 'enum': ['L', 'M', 'S']
    #     #             }
    #     #
    #     #         },
    #     #         "required": ['color', 'size']
    #     #     }
    #     #     form.base_fields['variant'].widget.attrs['cols'] = 10
    #     #
    #     #     form.base_fields['variant'].widget = JSONEditorWidget(DATA_SCHEMA, False)
    #     #     yield inline
    #     formsets = super(ProductModelAdmin, self).get_formsets_with_inlines(request, obj)
    #     # for index,inline in enumerate(self.inlines):
    #     for inline in self.get_inline_instances(request, obj):
    #         if inline.model==ProductUnit:
    #
    #
    #             # Do stuff with the form
    #             DATA_SCHEMA = {
    #                 'type': 'object',
    #                 'title': 'Data',
    #                 'properties': {
    #
    #                     'color': {
    #                         'title': 'color',
    #                         'type': 'string',
    #                         'enum': ['red', 'blue', 'black']
    #                     },
    #                     'size': {
    #                         'title': 'size',
    #                         'type': 'string',
    #                         'enum': ['L', 'M', 'S']
    #                     }
    #
    #                 },
    #                 "required": ['color', 'size']
    #             }
    #             inline.form.base_fields['variant'].widget = JSONEditorWidget(DATA_SCHEMA, False)
    #             yield inline.get_formset(request, obj), inline
    #
    #
    #     # return formsets

    def save_model(self, request, obj, form, change):
        super(ProductModelAdmin, self).save_model(request, obj, form, change)

admin.site.register(Category,CategoryAdmin)
admin.site.register(Type)
admin.site.register(Brand)
admin.site.register(Supplier)
# admin.site.register(ProductUnit)