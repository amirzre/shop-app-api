from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from core.models import TimeStampedModel
from product.models import Product


class Cart(TimeStampedModel):
    """Cart object"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_cart',
        verbose_name=_('User')
    )
    total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, blank=True, null=True,
        verbose_name=_('Total')
    )

    def __str__(self):
        return f'{self.user.email} - {self.total}'


class CartItem(TimeStampedModel):
    """Cart item for cart model"""
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='cart_item',
        verbose_name=_('Cart')
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='cart_product',
        verbose_name=_('Product')
    )
    quantity = models.IntegerField(default=1, verbose_name=_('Quantity'))

    def __str__(self):
        return f'{self.product} - {self.quantity}'
