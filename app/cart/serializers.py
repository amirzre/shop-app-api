from rest_framework import serializers
from product.models import Product
from cart.models import CartItem


class CartProductSerializer(serializers.ModelSerializer):
    """Cart product serializer"""
    class Meta:
        model = Product
        fields = (
            'id', 'uuid', 'seller', 'title', 'price', 'image'
        )


class CartItemSerializer(serializers.ModelSerializer):
    """Cart item serializer"""
    class Meta:
        model = CartItem
        fields = ('cart', 'product', 'quantity')
