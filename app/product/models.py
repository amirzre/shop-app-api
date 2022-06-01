from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from core.models import TimeStampedModel, Extensions


def category_image_path(instance, filename):
    return "category/icons/{}/{}".format(instance.name, filename)


def product_image_path(instance, filename):
    return "product/images/{}/{}".format(instance.title, filename)


class Category(MPTTModel):
    """Category to be used for a product"""
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    icon = models.ImageField(
        upload_to=category_image_path,
        blank=True, verbose_name=_('Icon')
    )
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, related_name='children',
        null=True, blank=True, verbose_name=_('Parent')
    )
    created = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Created Time')
    )
    modified = models.DateTimeField(
        auto_now=True, verbose_name=_('Modified Time')
    )

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(Extensions):
    """Product object"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_product',
        verbose_name=_('User')
    )
    category = TreeForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='product_category',
        verbose_name=_('Category')
    )
    title = models.CharField(max_length=250, verbose_name=_('Name'))
    price = models.DecimalField(
        decimal_places=2, max_digits=10,
        null=True, blank=True, verbose_name=_('Price')
    )
    image = models.ImageField(
        upload_to=product_image_path, blank=True, verbose_name=_('Image')
    )
    description = models.TextField(
        null=True, blank=True, verbose_name=_('Description')
    )
    quantity = models.IntegerField(default=1, verbose_name=_('Quantity'))
    views = models.IntegerField(default=0, verbose_name=_('Views'))
    is_deleted = models.BooleanField(
        default=False, verbose_name=_('Is Delete?')
    )

    def __str__(self):
        return str(self.uuid)


class Review(TimeStampedModel):
    """User comment fo each product"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='product_review',
        verbose_name=_('Product'),
        null=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_review',
        verbose_name=_('User'),
    )
    name = models.CharField(
        max_length=100,
        verbose_name=_('Name')
    )
    rating = models.IntegerField(
        default=0,
        verbose_name=_('Rating')
    )
    comment = models.TextField(verbose_name='Comment')

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return str(self.rating)


class ProductViews(TimeStampedModel):
    """Track product views"""
    ip = models.CharField(max_length=250, verbose_name=_('IP Address'))
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="product_views",
        verbose_name=_('Product')
    )

    class Meta:
        verbose_name = 'Product Views'
        verbose_name_plural = 'Product Views'

    def __str__(self):
        return f"{self.ip} - {self.product}"
