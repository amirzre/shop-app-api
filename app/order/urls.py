from django.urls import path
from order import views


app_name = 'order'

urlpatterns = [
    path('list/', views.ListOrdersApiView.as_view(), name='list'),
    path('create/', views.CreateOrderItemsApiView.as_view(), name='create'),
    path('user-order/', views.ListOrdersApiView.as_view(), name='user_order'),
    path('<int:pk>/', views.RetrieveOrderApiView.as_view(), name='order'),
    path('<int:pk>/pay/',
         views.UpdateOrderToPaidApiView.as_view(),
         name='order_pay'
         ),
    path(
        '<int:pk>/deliver/',
        views.UpdateOrderToDeliveredApiView.as_view(),
        name='order_deliver'
    ),
]
