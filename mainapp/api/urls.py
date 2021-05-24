from django.urls import path
from .api_views import CategoryListView, SmartphoneListView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('smartphones/', SmartphoneListView.as_view(), name='smartphones'),
]
