import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import AttribiutFormSet,Catform
from genson import SchemaBuilder
from .models import Category, Type, Brand, Product
import hashlib
from .serializers import (ProductListSerializer,
                          ProductDetaileSerializer)

from rest_framework import viewsets
from .permissions import IsSupplierOrAdminOrReadonly


def __create_shema(attnames, atttypes, catname):
    b1=SchemaBuilder()
    shema_name=int(hashlib.sha1(catname.encode('utf-8')).hexdigest(), 16) % (10 ** 8)

    for i,name in enumerate(attnames):
        b1.add_schema({"type": "object", "properties": {"{0}".format(name): {"type": "{0}".format(atttypes[i])}}})
    b1.add_schema({"required":attnames})

    shema=str(b1.to_json())
    # with codecs.open('attSchemas/{0}.json'.format(shema_name),'w', 'utf-8') as fp:
    #     fp.write(json.dumps(shema, ensure_ascii=False))

    with open('attSchemas/{0}.json'.format(shema_name),'w',encoding='utf8') as f:
        f.write(shema)
    # b1.to_json('attSchemas/{0}.json'.format(shema_name))
    return '{0}.json'.format(shema_name)

# TODO: add validations for repeative category name
# TODO:should be part of admin page


class add_category(APIView):
    permission_classes = [IsAuthenticated,]
    def __create_shema(attnames, atttypes, catname):
        b1 = SchemaBuilder()
        shema_name = int(hashlib.sha1(catname.encode('utf-8')).hexdigest(), 16) % (10 ** 8)

        for i, name in enumerate(attnames):
            b1.add_schema({"type": "object", "properties": {"{0}".format(name): {"type": "{0}".format(atttypes[i])}}})
        b1.add_schema({"required": attnames})

        shema = str(b1.to_json())
        # with codecs.open('attSchemas/{0}.json'.format(shema_name),'w', 'utf-8') as fp:
        #     fp.write(json.dumps(shema, ensure_ascii=False))

        with open('attSchemas/{0}.json'.format(shema_name), 'w', encoding='utf8') as f:
            f.write(shema)
        # b1.to_json('attSchemas/{0}.json'.format(shema_name))
        return '{0}.json'.format(shema_name)
    template_name = 'shema.html'
    heading_message = 'افزودن ویژگی'
    def get(self,request):
        formset = AttribiutFormSet(request.GET or None)
        catform = Catform(request.GET or None)
        return render(request, self.template_name, {
            'catform': catform,
            'formset': formset,
            'heading': self.heading_message,
        })


    def post(self,request):
        attnames = []
        atttypes = []

        formset = AttribiutFormSet(request.POST)
        catform = Catform(request.POST)
        if formset.is_valid():
            for form in formset:
                name = form.cleaned_data.get('name')
                atype = form.cleaned_data.get('att_type')
                # save book instance
                if name:
                    attnames.append(name)
                    atttypes.extend(atype)
            shema = self.__create_shema(attnames=attnames, atttypes=atttypes, catname=request.POST.get('category_name'))

            newcat = Category(category_name=request.POST.get('category_name'),
                              type=Type.objects.get(id=int(request.POST.get('type'))),
                              attributes_Schema_name=shema)
            newcat.save()
            catform = Catform(None)
            formset = AttribiutFormSet(None)

        return render(request, self.template_name, {
            'catform': catform,
            'formset': formset,
            'heading': self.heading_message,
        })



def get_brands(request):
    id=request.GET.get('id','')
    result=list(Brand.objects.filter(category_id=int(id)).values('id','brand_name'))
    return HttpResponse(json.dumps(result),content_type="application/json")



# TODO : should fix bug in post in list page
# TODO: add caching to view set ...

class ProductListViewSet(viewsets.ViewSet):


    def list(self, request):


        queryset = Product.objects.all()
        serializer = ProductListSerializer(queryset,many=True)
        return Response(serializer.data)


    def retrieve(self, request, pk=None):

        queryset = Product.objects.all()
        product=get_object_or_404(queryset,pk=pk)
        serializer = ProductDetaileSerializer(product)
        return Response(serializer.data)



# TODO: list product by category| search based on category values  shcema
# TODO: list prouct sort by (price|num of orders)





