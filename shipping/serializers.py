from django.db.models import F
from rest_framework import serializers

from cart.cart import Cart
from cart.models import ShoppingCart
from content.models import ProductUnit
from shipping.models import Order, OrderItem
from shop import settings
from users.models import Adress
from users.serializers import AddressSerializer

class OrderItemSerilizer(serializers.ModelSerializer):


    class Meta:
        model = OrderItem
        fields = ('order',
                  'product_unit',
                  'quantity',
                  'main_image_path',
                  'product_name',
                  'product_unit_price',
                  'seller')

class OrderSerializer(serializers.ModelSerializer):
    # orderItems = serializers.SerializerMethodField()

    # def get_orderItems(self,request):
    #
    #     cart = Cart(request=request)
    #     for item in cart:

    # def create(self, validated_data):
    #     request = self.context.get('request')
    #     address_id = request.data['addressid']
    #     customer = request.user
    #
    #     order = Order.objects.create(**data)

    # order_items = OrderItemSerilizer(read_only=True, many=True)

    class Meta:
        model = Order
        fields =('address',)
    def create(self, validated_data):
        request = self.context.get('request')
        address_id = request.data['addressid']
        customer = request.user
        # order_items = validated_data.pop('order_items')

        cartinstance = Cart(request=request)

        # check quantity
        for item in cartinstance.cart.items():
            product_unit = ProductUnit.objects.get(id= item[0])
            quantity = item[1]['quantity']
            if quantity > product_unit.storage_count:
                raise serializers.ValidationError('not enough number of {0}'
                                                  ' in stoke({1} number '
                                                  'is available'.format(product_unit.product.name,
                                                                        product_unit.storage_count))
        # quantity is ok now order should be create
        order = Order.objects.create(customer=customer,
                                     address=Adress.objects.get(id=address_id),
                                     shipping_status=Order.PENDING,
                                     total_price=cartinstance.get_total_price())

        for item in cartinstance.cart.items():
            product_unit = ProductUnit.objects.get(id= item[0])
            quantity = item[1]['quantity']
            OrderItem.objects.create(
                order = order,
                product_unit = product_unit,
                quantity = quantity,
                main_image_path = product_unit.product.images.filter(is_default_pic=True)[0].image_path,
                product_name = product_unit.product.name,
                product_unit_price= product_unit.price,
                seller = product_unit.seller.name
            ).save()

        # update storage cout of product
        product_unit.storage_count = F('storage_count') - quantity
        product_unit.save()

        # empty cart session and cart in database
        cartinstance.clear()
        userShopCart = ShoppingCart.objects.get(customer=customer)
        userShopCart.cart_session=None
        userShopCart.save(update_fields=['cart_session'])

        return order


