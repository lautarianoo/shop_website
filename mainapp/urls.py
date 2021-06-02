from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', HomeBaseView.as_view(), name='base'),
    path('products/<str:slug>/', ProductDetailView.as_view(), name="product_detail"),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:slug>/', AddtoCartView.as_view(), name='add_to_card'),
    path('remove-from-cart/<str:slug>/', DeleteFromCartView.as_view(), name='delete_from_card'),
    path('changeqty-from-cart/<str:slug>/', ChangeQTYView.as_view(), name='change_qty_from_card'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('makeorder/', MakeOrderView.as_view(), name='make_order'),
    path('payed-online-order/', PayedOnlineOrderView.as_view(), name='payed_online'),
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
