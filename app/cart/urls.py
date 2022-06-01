from django.urls import path
from cart import views


app_name = 'cart'

urlpatterns = [
    path('create/', views.CreateCartItemApiView.as_view(), name='create'),
    path('cart-item/<int:pk>/',
         views.RetrieveUpdateDestroyCartItemApiView.as_view(),
         name='cart_item'
         ),
]
