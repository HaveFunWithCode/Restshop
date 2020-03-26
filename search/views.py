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
from django.db.models import Q


class SearchView(APIView,LoadShemaMixin):
    permission_classes = [AllowAny]
    # throttle_classes = (UserRateThrottle,)
    # throttle_scope = 'search-category'

    def get(self,request,catid):
        # get schema for category
        CATEGORY_SCHEMA=self.load_schema(catid)
        # get all searchable type fields
        enum_fields = [[a, CATEGORY_SCHEMA["properties"][a]['enum']] for a in CATEGORY_SCHEMA["properties"] if
                      'enum' in CATEGORY_SCHEMA["properties"][a]]
        string_fields = [[a, CATEGORY_SCHEMA["properties"][a]] for a in CATEGORY_SCHEMA["properties"] if
                        CATEGORY_SCHEMA["properties"][a]['type'] =='string' and
                        'enum' not in CATEGORY_SCHEMA["properties"][a]]
        int_fields = [[a, CATEGORY_SCHEMA["properties"][a]] for a in CATEGORY_SCHEMA["properties"]
                      if CATEGORY_SCHEMA["properties"][a]['type']=='integer']
        boolean_fields = [[a, CATEGORY_SCHEMA["properties"][a]] for a in CATEGORY_SCHEMA["properties"] if
                          CATEGORY_SCHEMA["properties"][a]['type']=='boolean' ]


        enum_search_filters = [a[0] for a in enum_fields]
        enum_search_filters_possible_values=[[attr[1] for attr in enum_fields]]

        string_search_filters = [a[0] for a in string_fields]
        boolean_search_filters = [a[0] for a in boolean_fields]

        integer_search_filters = [a[0] for a in int_fields]

        category_criterion = Q(category_id=catid)

        if len(request.GET)==0:
            queryset = Product.objects.filter(category_criterion)
            serializer = ProductListSerializer(queryset, many=True)
        else:
            filters = {k:val for k, val in request.GET.items()}

            # build queryset criterion

            finalQuery = category_criterion
            other_criterions=[]
            for filter,_ in filters.items():
                if filter in enum_search_filters:
                    # search in product units
                    other_criterions.append(Q(product_unit__variant__contains={filter: filters[filter]}))

                elif filter in string_search_filters:
                    # search in json_field string values
                    other_criterions.append(Q(values__contains = {filter: filters[filter]}))

                elif filter in boolean_search_filters:
                    other_criterions.append(Q(values__contains = {filter:bool(filters[filter])}))

            for q in other_criterions:
                finalQuery  &= q
            queryset = Product.objects.filter(category_criterion & finalQuery)
            serializer = ProductListSerializer(queryset, many=True)

        return Response({'search_result_incategory': serializer.data,
                        'search_posible_filters':
                             {'enum_search_filters': enum_fields,
                              'enum_search_filters_possible_values': enum_search_filters_possible_values,
                              'stringfields': string_fields,
                              'booleanfileds': boolean_fields}

                         })

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


