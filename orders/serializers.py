from django.db import transaction
from rest_framework import serializers

from orders.models import Order, Whishlist
from products.models import Product
from products.serializers import ProductSerializer
from users.models import User
from users.serializers import UserDetailsSerializer


class OrdersSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)
    product = ProductSerializer(read_only=True, many=False)
    user = UserDetailsSerializer(read_only=True, many=False)

    class Meta:
        model = Order
        fields = ('product', 'user', 'product_id', 'created_at', 'updated_at')

    def create(self, validated_data):
        with transaction.atomic():
            product_id = validated_data['product_id']

            product = Product.objects.get(id=product_id)
            user = User.objects.get(id=self.context.get('user_id'))
            print("\n\n --->>>>", product_id, self.context.get('user_id'))

            order_obj = Order.objects.create(
                product=product,
                user=user
            )
        return order_obj


class WishlistSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)
    product = ProductSerializer(read_only=True, many=False)
    user = UserDetailsSerializer(read_only=True, many=False)

    class Meta:
        model = Whishlist
        fields = ('product', 'user', 'product_id')

    def create(self, validated_data):
        with transaction.atomic():
            product_id = validated_data['product_id']

            product = Product.objects.get(id=product_id)
            user = User.objects.get(id=self.context.get('user_id'))

            wishlist_obj = Whishlist.objects.create(
                product=product,
                user=user
            )
        return wishlist_obj
