from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from core.models import TimeStampedModel, Extensions
from product.models import Product


class Order(Extensions):
    """Order object"""
    PENDING_STATE = 'p'
    COMPLETED_STATE = 'c'

    ORDER_CHOICES = (
        (PENDING_STATE, 'pending'),
        (COMPLETED_STATE, 'completed')
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='order',
        verbose_name=_('User')
    )
    payment_method = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_('Payment Method')
    )
    tax_price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_('Tax Price')
    )
    shipping_price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_('Shipping Price')
    )
    total_price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_('Total Price')
    )
    is_paid = models.BooleanField(default=False, verbose_name=_('Is Paid?'))
    paid_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Paid Time')
    )
    is_deliverd = models.BooleanField(
        default=False, verbose_name=_('Is Deliverd?')
    )
    deliverd_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Deliverd Time')
    )
    status = models.CharField(
        max_length=1,
        choices=ORDER_CHOICES,
        default=PENDING_STATE,
        verbose_name=_('Status')
    )

    def __str__(self):
        return f"{self.user} - {self.total_price}"


class OrderItem(TimeStampedModel):
    """Order item object"""
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name=_('Order')
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_order',
        verbose_name=_('Product')
    )
    name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_('Name')
    )
    quantity = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=_('Quantity')
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_('Price')
    )

    def __str__(self):
        return f"{self.order} - {self.product}"


class ShippingAddress(models.Model):
    """Shipping Address object"""
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='shipping_order',
        verbose_name=_('Order')
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_('Address')
    )
    city = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_('City')
    )
    country = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name=_('Country')
    )
    postal_code = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_('Postal Code')
    )
    shipping_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name=_('Shipping Price')
    )

    def __str__(self):
        return self.address
