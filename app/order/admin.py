from django.contrib import admin
from order.models import Order, OrderItem, ShippingAddress


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'payment_method', 'tax_price', 'shipping_price', 'total_price',
        'status', 'is_paid', 'is_deliverd', 'paid_at', 'deliverd_at'
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'order', 'product', 'name', 'quantity', 'price'
    )


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = (
        'order', 'address', 'city', 'country', 'postal_code', 'shipping_price'
    )
