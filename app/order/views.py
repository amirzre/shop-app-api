from datetime import datetime
from rest_framework.generics import (
    ListCreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from product.models import Product
from order.models import Order, OrderItem, ShippingAddress
from order.serializers import OrderSerializer


class CreateOrderItemsApiView(ListCreateAPIView):
    """Create order item"""
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        order_items = data['order_items']

        if order_items and len(order_items) == 0:
            return Response(
                {'detail': 'No Order Items'},
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            order = Order.objects.create(
                user=user,
                payment_method=data['payment_method'],
                tax_price=data['tax_price'],
                shipping_price=data['shipping_price'],
                total_price=data['total_price']
            )

            shipping = ShippingAddress.objects.create(
                order=order,
                address=data['shippingAddress']['address'],
                city=data['shippingAddress']['city'],
                postalCode=data['shippingAddress']['postalCode'],
                country=data['shippingAddress']['country']
            )

            for item in order_items:
                product = Product.objects.get(id=item['product'])
                item = OrderItem.objects.create(
                    product=product,
                    order=order,
                    name=product.name,
                    quantity=item['quantity'],
                    price=item['price'],
                )

                product.quantity -= item.quantity
                product.save()

            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ListUserOrdersApiView(ListAPIView):
    """Retrieve list user orders"""
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        orders = user.order.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class ListOrdersApiView(ListAPIView):
    """Retrieve list orders"""
    permission_classes = (IsAdminUser,)
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class RetrieveOrderApiView(RetrieveAPIView):
    """Retrieve an order"""
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer

    def get(self, request, pk, *args, **kwargs):
        user = request.user
        try:
            order = Order.objects.get(id=pk)
            if user.is_staff or order.user == user:
                serializer = OrderSerializer(order, many=False)
                return Response(serializer.data)
            else:
                return Response(
                    {'detail': 'Not authorized to view this order!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception:
            return Response(
                {'detail': 'Order does not exist!'},
                status=status.HTTP_400_BAD_REQUEST
            )


class UpdateOrderToPaidApiView(UpdateAPIView):
    """Update order to paid status"""
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer

    def put(self, request, pk, *args, **kwargs):
        order = Order.objects.get(id=pk)
        order.is_paid = True
        order.paid_at = datetime.now()
        order.save()
        return Response('Order was paid!')


class UpdateOrderToDeliveredApiView(UpdateAPIView):
    """Update order to delivered status"""
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer

    def put(self, request, pk, *args, **kwargs):
        order = Order.objects.get(id=pk)
        order.is_deliverd = True
        order.deliverd_at = datetime.now()
        order.save()
        return Response('Order was delivered!')
