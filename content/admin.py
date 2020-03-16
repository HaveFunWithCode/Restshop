import json
from django import forms
from django.contrib import admin
from jsonschemaform.admin.widgets.jsonschema_widget import JSONSchemaWidget
from .models import Category, Product, Type, Brand, ProductUnit, SupplierUser, Image


class productImageInline(admin.StackedInline):
    model = Image
    extra = 1
    verbose_name = 'افزودن تصاویر'
    verbose_name_plural = 'تصاویر محصول'


class CategoryAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CategoryAdminForm, self).__init__(*args, **kwargs)
        self.fields['type'].widget = JSONSchemaWidget()

    class Meta:
        model = Category
        fields = "__all__"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'type', 'attributes_Schema_name')
    list_filter = ['type']


class VariantsWidget(forms.MultiWidget):

    def __init__(self, dict, attrs=None):
        w = []

        for key, val in dict.items():
            w.append(forms.Select(choices=tuple([(val, val) for val in val]), attrs={'name': key}))
        widgets = tuple(w)
        super(VariantsWidget, self).__init__(widgets, attrs)

    # decompress jsonfiled
    def decompress(self, value):
        # TODO: bug fix can not load properly
        if value != 'null':
            return list(dict(json.loads(value)).values())
        return len(self.widgets) * [None]

    # returns a list  of  values corresponding  to each  Widget( it should implement when we don not want to user MultiField)
    def value_from_datadict(self, data, files, name):

        variants = dict()
        for i, widget in enumerate(self.widgets):
            variants[widget.attrs['name']] = super(VariantsWidget, self).value_from_datadict(data, files, name)[0]
        if len(variants.values()) > 0:
            return json.dumps(variants)


def load_schema(cat_id):
    DATA_SCHEMA_name = Category.objects.values_list('attributes_Schema_name', flat=True).get(id=int(cat_id))
    with open("attSchemas/{0}".format(DATA_SCHEMA_name)) as jfile:
        return json.load(jfile)


class productUnitJsonForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):

        super(productUnitJsonForm, self).__init__(*args, **kwargs)
        if 'catid' in self.Meta.formfield_callback.keywords['request'].GET:
            cat_id = self.Meta.formfield_callback.keywords['request'].GET['catid']
        else:
            first_cat_row = Category.objects.values_list('id', flat=True).first()
            cat_id = kwargs.get('instance').product.category_id if 'instance' in kwargs else first_cat_row

        DATA_SCHEMA = load_schema(cat_id)
        enumfields = [[a, DATA_SCHEMA["properties"][a]['enum']] for a in DATA_SCHEMA["properties"] if
                      'enum' in DATA_SCHEMA["properties"][a]]

        names = [a[0] for a in enumfields]
        values = [a[1] for a in enumfields]

        self.fields['variant'].widget = VariantsWidget(dict(zip(names, values)))

    class Meta:
        model = ProductUnit
        fields = "__all__"


class productUnitInline(admin.StackedInline):
    model = ProductUnit
    form = productUnitJsonForm
    extra = 0
    fields = ["variant", "variant_title", "seller", "price", "storage_count"]

    def get_formset(self, request, obj=None, **kwargs):
        return super(productUnitInline, self).get_formset(request, obj, **kwargs)


# TODO: add validation to product filed
# TODO: add variations to product filed
#
class ProductJSONModelAdminForm(forms.ModelForm):

    def __init__(self, *args, request=None, **kwargs):
        # load schema based on cat seleted
        if 'instance' in kwargs and kwargs['instance'] != None:
            cat_id = kwargs['instance'].category.id
        else:
            first_cat_row = Category.objects.values_list('id', flat=True).first()
            cat_id = int(kwargs.get('initial')['catid']) if 'initial' in kwargs and 'catid' in kwargs.get(
                'initial') else (
                int(args[0].get('category')) if len(args) > 0 and 'category' in args[0] else first_cat_row)
        DATA_SCHEMA = load_schema(cat_id)

        super().__init__(*args, **kwargs)

        self.initial['category'] = cat_id
        self.fields['brand'].queryset = Brand.objects.filter(category_id=cat_id)
        self.fields['values'].widget = JSONSchemaWidget(DATA_SCHEMA)

    class Meta:
        model = Product
        fields = "__all__"


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'id']
    form = ProductJSONModelAdminForm
    inlines = [productUnitInline, productImageInline]
    change_form_template = "content/my_product_admin.html"

    def save_model(self, request, obj, form, change):
        super(ProductModelAdmin, self).save_model(request, obj, form, change)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Type)
admin.site.register(Brand)
admin.site.register(SupplierUser)
