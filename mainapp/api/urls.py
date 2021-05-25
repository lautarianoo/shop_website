from django.urls import path
from .api_views import CategoryListView, SmartphoneListView, NotebookListView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('smartphones/', SmartphoneListView.as_view(), name='smartphones'),
    path('notebooks/', NotebookListView.as_view(), name='notebooks')
]
