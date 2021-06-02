from django.urls import path
from .views import *


urlpatterns = [
    path('', BaseSpecView.as_view(), name='base_spec'),
    path('add-category/', NewCategoryView.as_view(), name='add_category')
]
