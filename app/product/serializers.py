from django.contrib.auth import get_user_model
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from product.models import Category, Product, ProductViews, Review


class CategorySerializer(serializers.ModelSerializer):
    """Category model serializer"""
    class Meta:
        model = Category
        fields = (
            'id', 'name', 'icon', 'parent', 'created', 'modified'
        )


class ReviewSerializer(serializers.ModelSerializer):
    """Review model serializer"""
    class Meta:
        model = Review
        fields = (
            'id', 'user', 'product', 'title', 'rating', 'comment', 'created'
        )


class ProductSerializer(serializers.ModelSerializer):
    """Product model serializer"""
    user = serializers.SlugRelatedField(
        slug_field='email',
        queryset=get_user_model().objects
    )
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Category.objects
    )
    image = Base64ImageField()
    reviews = serializers.SerializerMethodField(read_only=True)

    def get_category(self, obj):
        return obj.category.name

    def get_reviews(self, obj):
        reviews = obj.product_review.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data

    class Meta:
        model = Product
        fields = (
            'id', 'uuid', 'user', 'title', 'price', 'category',
            'description', 'quantity', 'image', 'views', 'is_deleted',
            'reviews'
        )


class ProductViewsSerializer(serializers.ModelSerializer):
    """View product serializer"""
    class Meta:
        model = ProductViews
        fields = ('id', 'ip', 'product', 'created', 'modified')
