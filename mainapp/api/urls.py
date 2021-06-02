from django.urls import path
from .api_views import CategoryAPIView #SmartphoneListView, NotebookListView, SmartphoneDetailView, NotebookDetailView

urlpatterns = [
    path('categories/<str:id>/', CategoryAPIView.as_view(), name='categories'),
    #path('smartphones/', SmartphoneListView.as_view(), name='smartphones'),
    #path('notebooks/', NotebookListView.as_view(), name='notebooks'),
    #path('smartphones/<str:pk>/', SmartphoneDetailView.as_view(), name='smartphone_detail'),
    #path('notebooks/<str:pk>/', NotebookDetailView.as_view(), name='notebook_detail')
]#
