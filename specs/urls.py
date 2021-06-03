from django.urls import path
from .views import *


urlpatterns = [
    path('', BaseSpecView.as_view(), name='base_spec'),
    path('add-category/', NewCategoryView.as_view(), name='add_category'),
    path('new-feature/', NewFeatureView.as_view(), name='new_feature'),
    path('new-feature-product/', NewFeatureProductView.as_view(), name='new_feature_product'),
]
