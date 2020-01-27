from django.contrib import admin
from .models import Category,Product,Type,Brand,ProductUnit,Supplier,Image



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

admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Type)
admin.site.register(Brand)
admin.site.register(Supplier)
admin.site.register(ProductUnit)


# Register your models here.
