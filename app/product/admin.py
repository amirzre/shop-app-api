from django.contrib import admin
from product.models import Category, Product, ProductViews, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'created', 'modified')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'price', 'quantity', 'category', 'user', 'views',
        'is_deleted'
    )
    list_editable = ('is_deleted',)


@admin.register(ProductViews)
class ProductViewsAdmin(admin.ModelAdmin):
    list_display = ('ip', 'product', 'created')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'product', 'rating', 'created')
