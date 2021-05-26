from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from .serializers import CategorySerializer, SmartphoneSerializer, NotebookSerializer
from..models import Category, SmartPhone, Notebook
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict

class CategoryPagination(PageNumberPagination):

    page_size = 2
    page_query_param = 'page_size'
    max_page_size = 10

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('items', data)
        ]))

class CategoryAPIView(ListCreateAPIView, RetrieveUpdateAPIView):

    serializer_class = CategorySerializer
    pagination_class = CategoryPagination
    queryset = Category.objects.all()
    lookup_field = 'id'

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

class SmartphoneDetailView(RetrieveAPIView):

    serializer_class = SmartphoneSerializer
    queryset = SmartPhone.objects.all()

class NotebookDetailView(RetrieveAPIView):

    serializer_class = NotebookSerializer
    queryset = Notebook.objects.all()
