from rest_framework.generics import ListAPIView
from .serializers import CategorySerializer, SmartphoneSerializer, NotebookSerializer
from..models import Category, SmartPhone, Notebook
from rest_framework.filters import SearchFilter

class CategoryListView(ListAPIView):

    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class SmartphoneListView(ListAPIView):

    serializer_class = SmartphoneSerializer
    queryset = SmartPhone.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['price', 'title']

class NotebookListView(ListAPIView):

    serializer_class = NotebookSerializer
    queryset = Notebook.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['price', 'title']
