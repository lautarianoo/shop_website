from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeBaseView.as_view(), name='base'),
    path('products/<str:ct_model>/<str:slug>/', ProductDetailView.as_view(), name="product_detail"),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:ct_model>/<str:slug>/', AddtoCartView.as_view(), name='add_to_card'),
    path('remove-from-cart/<str:ct_model>/<str:slug>/', DeleteFromCartView.as_view(), name='delete_from_card'),
    path('changeqty-from-cart/<str:ct_model>/<str:slug>/', ChangeQTYView.as_view(), name='change_qty_from_card'),
]
