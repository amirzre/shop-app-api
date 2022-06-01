from django.urls import path
from product import views


app_name = 'product'

urlpatterns = [
    path("list/", views.ListProductAPIView.as_view(), name='list'),
    path('create/', views.CreateProductApiView.as_view(), name='create'),
    path('detail/<int:pk>/',
         views.RetrieveUpdateDestroyProductApiView.as_view(),
         name='detail'
         ),
    path('top/', views.RetrieveTopProductApiView.as_view(), name='top'),
    path("category/list/",
         views.CategoryListAPIView.as_view(),
         name='category_list'
         ),
    path("category/create/",
         views.CreateCategoryApiView.as_view(),
         name='category_create'
         ),
    path("category/detail/<int:pk>/",
         views.RetrieveUpdateDestroyCategoryApiView.as_view(),
         name='category_detail'
         ),
    path('reviews/<int:pk>/',
         views.CreateProductReviewApiView.as_view(),
         name='create_review'
         ),
]
