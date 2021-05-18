from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='base'),
    path('products/<str:ct_model>/<str:slug>/', ProductDetailView.as_view(), name="product_detail"),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category_detail')
]
