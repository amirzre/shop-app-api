from rest_framework import serializers
from user.serializers import UserSerializer
from order.models import Order, OrderItem, ShippingAddress


class OrderItemSerializer(serializers.ModelSerializer):
    """Order item serializer"""
    class Meta:
        model = OrderItem
        fields = (
            'order', 'product', 'name', 'name', 'quantity', 'price'
        )


class ShippingAddressSerializer(serializers.ModelSerializer):
    """ShippingAddress serializer"""
    class Meta:
        model = ShippingAddress
        fields = (
            'order', 'address', 'city', 'country', 'postal_code',
            'shipping_price'
        )


class OrderSerializer(serializers.ModelSerializer):
    """Order serializer"""
    order_items = serializers.SerializerMethodField(read_only=True)
    shipping_address = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = (
            'id', 'user', 'payment_method', 'tax_price', 'shipping_price',
            'total_price', 'order_items', 'status', 'is_paid', 'is_deliverd',
            'paid_at', 'deliverd_at', 'shipping_address', 'created'
        )

    def get_order_items(self, obj):
        items = obj.order_items.all()
        serializer = OrderItemSerializer(items, many=True)
        return serializer.data

    def get_shipping_address(self, obj):
        try:
            address = ShippingAddressSerializer(
                obj.shippingaddress, many=False).data
        except Exception:
            address = False
        return address

    def get_user(self, obj):
        user = obj.user
        serializer = UserSerializer(user, many=False)
        return serializer.data
