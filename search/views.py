from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle,UserRateThrottle
from rest_framework.views import APIView
from content.mixins import LoadShemaMixin
from content.models import Product
from content.serializers import ProductListSerializer, ProductDetaileSerializer


class SearchView(APIView,LoadShemaMixin):
    permission_classes = [AllowAny]
    # throttle_classes = (UserRateThrottle,)
    # throttle_scope = 'search-category'

    def get(self,request,catid):
        # get schema for category

        CATEGORY_SCHEMA=self.load_schema(catid)

        # get all searchable type fields
        enumfields = [[a, CATEGORY_SCHEMA["properties"][a]['enum']] for a in CATEGORY_SCHEMA["properties"] if
                      'enum' in CATEGORY_SCHEMA["properties"][a]]
        stringfields = [[a, CATEGORY_SCHEMA["properties"][a]] for a in CATEGORY_SCHEMA["properties"] if
                        CATEGORY_SCHEMA["properties"][a]['type'] =='string' and
                        'enum' not in CATEGORY_SCHEMA["properties"][a]]

        intfields = [[a, CATEGORY_SCHEMA["properties"][a]] for a in CATEGORY_SCHEMA["properties"] if CATEGORY_SCHEMA["properties"][a]['type']=='integer' ]
        booleanfields = [[a, CATEGORY_SCHEMA["properties"][a]] for a in CATEGORY_SCHEMA["properties"] if CATEGORY_SCHEMA["properties"][a]['type']=='boolean' ]


        enum_search_filters=[a[0] for a in enumfields]
        enum_search_filters_possible_values=[[attr[1] for attr in enumfields]]
        # string_search_filters=[a[0] for a in stringfields]

        if request.GET == None:
            return Response({'enum_search_filters':enumfields, 'enum_search_filters_possible_values':enum_search_filters_possible_values,'stringfields':stringfields})
        else:
            final_query_string = {}
            filters = {k:val for k,val in request.GET.items()}
            for filter,_ in filters.items():
                if filter in enum_search_filters:
                    # search in product units
                    pass
                elif filter in stringfields:
                    # create string query
                    pass
                elif filter in intfields:
                    # creat string query
                    pass
                elif filter in booleanfields:
                    # creat string query
                    pass
            queryset = Product.objects.filter(category__id=catid, values__contains=final_query_string)
            serializer = ProductListSerializer(queryset, many=True)
            return Response(serializer.data)



        # return Response({'enumfields':enumfields, 'stringfields':stringfields, 'intfields':intfields, 'booleanfields':booleanfields})
        # return list of products for this category
        # return list of filters


class ProductListBasedOnCatViewSet(viewsets.ViewSet):

    def list(self,request, catid, attr_name,att_value):
        queryset = Product.objects.filter(category__id=catid, values__contains={attr_name:att_value})
        serializer = ProductListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Product.objects.all()
        product = get_object_or_404(queryset, pk=pk)
        serializer = ProductDetaileSerializer(product)
        return Response(serializer.data)


