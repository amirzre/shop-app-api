from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from product.serializers import (
    CategorySerializer,
    ProductSerializer,
    ReviewSerializer
)
from product.permissions import IsSuperUser, IsSuperUserOrReadOnly
from product.models import Category, Product, Review, ProductViews


class CategoryListAPIView(ListAPIView):
    """List of all categories"""
    permission_classes = (AllowAny,)
    serializer_class = CategorySerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    search_fields = ("name",)
    ordering_fields = ("created",)
    filter_fields = ("created",)
    queryset = Category.objects.all()


class CreateCategoryApiView(CreateAPIView):
    """Creates a new category"""
    permission_classes = (IsSuperUser,)
    serializer_class = CategorySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                serializer.data,
                status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status.HTTP_400_BAD_REQUEST
        )


class RetrieveUpdateDestroyCategoryApiView(RetrieveUpdateDestroyAPIView):
    """Retrieve, update and delete a category"""
    permission_classes = (IsSuperUser,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ListProductAPIView(ListAPIView):
    """List of products"""
    permission_classes = (AllowAny,)
    serializer_class = ProductSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    )
    search_fields = ('title',)
    ordering_fields = ('created',)
    filter_fields = ('views',)

    def get_queryset(self):
        queryset = Product.objects.filter(is_deleted=False)
        return queryset


class CreateProductApiView(CreateAPIView):
    """Creates a new product"""
    permission_classes = (IsSuperUser,)
    serializer_class = ProductSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(seller=user)
            return Response(
                serializer.data,
                status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status.HTTP_400_BAD_REQUEST
        )


class RetrieveUpdateDestroyProductApiView(RetrieveUpdateDestroyAPIView):
    """Retrieve, update and delete a product"""
    permission_classes = (IsSuperUser,)
    serializer_class = ProductSerializer

    def get(self, request, pk, *args, **kwargs):
        product = Product.objects.get(pk=pk)
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")

        if not ProductViews.objects.filter(product=product, ip=ip).exists():
            ProductViews.objects.create(product=product, ip=ip)

            product.views += 1
            product.save()
        serializer = ProductSerializer(
            product, context={"request": request})

        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        queryset = Product.objects.filter(is_deleted=False)
        return queryset


class RetrieveTopProductApiView(ListAPIView):
    """Retrieve 5 top products"""
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(views__gt=4)[0:5]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = Product.objects.filter(is_deleted=False)
        return queryset


class CreateProductReviewApiView(CreateAPIView):
    """Create a comment for product"""
    permission_classes = (IsSuperUserOrReadOnly,)
    serializer_class = ReviewSerializer

    def post(self, request, pk, *args, **kwargs):
        user = request.user
        data = request.data
        product = Product.objects.get(id=pk)

        already_exists = product.product_review.filter(user=user).exists()
        if already_exists:
            return Response(
                content={'detail': 'Product already reviewed!'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        elif data['rating'] == 0:
            return Response(
                content={'detail': 'Please select a rating!'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            review = Review.objects.create(
                user=user,
                title=user.name,
                product=product,
                rating=data['rating'],
                comment=data['comment']
            )
            reviews = product.product_review.all()
            product.views = len(reviews)

            total = 0
            for item in reviews:
                total += item.rating
            product.rating = total / len(reviews)
            product.save()

            return Response(
                content={'detail': 'Review added!'},
                status=status.HTTP_201_CREATED,
            )
