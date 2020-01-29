import json

from django.http import HttpResponse
from django.shortcuts import render
from .forms import AttribiutFormSet,Catform
from genson import SchemaBuilder
from .models import Category, Type, Brand
import hashlib

def create_shema(attnames,atttypes,catname):
    b1=SchemaBuilder()
    shema_name=int(hashlib.sha1(catname.encode('utf-8')).hexdigest(), 16) % (10 ** 8)

    for i,name in enumerate(attnames):
        b1.add_schema({"type": "object", "properties": {"{0}".format(name): {"type": "{0}".format(atttypes[i])}}})
    shema=str(b1.to_json())
    with open('attSchemas/{0}.json'.format(shema_name),'w',encoding='utf8') as f:
        f.write(shema)
    # b1.to_json('attSchemas/{0}.json'.format(shema_name))
    return '{0}.json'.format(shema_name)

# TODO: add validations for repeative category name
# TODO:should be part of admin page

def add_category(request):
    template_name = 'shema.html'
    heading_message = 'افزودن ویژگی'
    if request.method == 'GET':
        formset = AttribiutFormSet(request.GET or None)
        catform = Catform(request.GET or None)
    elif request.method == 'POST':
        attnames=[]
        atttypes=[]

        formset = AttribiutFormSet(request.POST)
        catform=Catform(request.POST)
        if formset.is_valid():
            for form in formset:
                name = form.cleaned_data.get('name')
                atype=form.cleaned_data.get('att_type')
                # save book instance
                if name:
                    attnames.append(name)
                    atttypes.extend(atype)
            shema=create_shema(attnames=attnames,atttypes=atttypes,catname=request.POST.get('category_name'))

            newcat=Category(category_name=request.POST.get('category_name'),
                            type=Type.objects.get(id=int(request.POST.get('type'))),
                            attributes_Schema_name=shema)
            newcat.save()
    return render(request, template_name, {
        'catform':catform,
        'formset': formset,
        'heading': heading_message,
    })


def get_brands(request):
    id=request.GET.get('id','')
    result=list(Brand.objects.filter(category_id=int(id)).values('id','brand_name'))
    return HttpResponse(json.dumps(result),content_type="application/json")

def get_attributes_Schema_name(request):
    id=request.GET.get('id','')
    shema_name=Category.objects.filter(id==int(id)).values('attributes_Schema_name')
    return shema_name

# def get_product_view(request):
#     id = request.GET.get('id', '')
#     form=Make_ProductJSONModelAdminForm(cat_id=int(id))