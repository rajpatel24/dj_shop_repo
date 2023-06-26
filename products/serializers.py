from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        # read_only = (
        #     'id', 'product_id', 'product_name', 'category', 'discounted_price', 'actual_price', 'discount_percentage',
        #     'rating', 'rating_count', 'about_product', 'img_link', 'created_at', 'updated_at'
        # )
        fields = (
            'id', 'product_id', 'product_name', 'category', 'discounted_price', 'actual_price', 'discount_percentage',
            'rating', 'rating_count', 'about_product', 'img_link', 'created_at', 'updated_at'
        )
