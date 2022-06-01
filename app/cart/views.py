from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotAcceptable,
    ValidationError,
    PermissionDenied
)
from product.models import Product
from cart.models import Cart, CartItem
from cart.serializers import CartItemSerializer


class CreateCartItemApiView(ListCreateAPIView):
    """Create cart item"""
    permission_classes = (permissions.AllowAny,)
    serializer_class = CartItemSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = CartItem.objects.filter(cart__user=user)
        return queryset

    def create(self, request, *args, **kwargs):
        user = request.user
        cart = get_object_or_404(Cart, user=user)
        product = get_object_or_404(Product, pk=request.data['product'])
        current_item = CartItem.objects.filter(cart=cart, product=product)

        if user == product.user:
            raise PermissionDenied('This is your product!')
        if current_item.count() > 0:
            raise NotAcceptable('You already have this item in your cart!')
        try:
            quantity = int(request.data['quantity'])
        except Exception:
            raise ValidationError('Please enter your quantity!')

        if quantity > product.quantity:
            raise NotAcceptable('You order quantity more than the seller have')

        cart_item = CartItem(cart=cart, product=product, quantity=quantity)
        cart_item.save()
        serializer = CartItemSerializer(cart_item)
        total = float(product.price) * float(quantity)
        cart.total = total
        cart.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class RetrieveUpdateDestroyCartItemApiView(RetrieveUpdateDestroyAPIView):
    """Retrieve, update and delete cart item"""
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()

    def retrieve(self, request, *args, **kwargs):
        cart_item = self.get_object()
        if cart_item.cart.user != request.user:
            raise PermissionDenied('Sorry this cart not belong to you!')
        serializer = self.get_serializer(cart_item)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        cart_item = self.get_object()
        product = get_object_or_404(Product, pk=request.data['product'])
        if cart_item.cart.user != request.user:
            return PermissionDenied('Sorry this cart not belong to you!')

        try:
            quantity = int(request.data['quantity'])
        except Exception:
            raise ValidationError('Please input valid quantity!')

        if quantity > product.quantity:
            raise NotAcceptable('Your order more than the seller have!')

        serializer = CartItemSerializer(cart_item, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        cart_item = self.get_object()
        if cart_item.cart.user != request.user:
            return PermissionDenied('Sorry this cart not belong to you!')
        cart_item.delete()
        return Response(
            {'detail': _('Your item has been deleted!')},
            status=status.HTTP_204_NO_CONTENT,
        )
