from django.shortcuts import render
from django.views.generic import DetailView, View
from .models import Notebook, SmartPhone, Category, LatestProducts
from .mixins import CategoryDetailMixin

class HomeBaseView(View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_category_for_left_sidebar()
        products = LatestProducts.objects.get_products_for_mainpage('notebook', 'smartphone')
        return render(request, 'mainapp/base.html', {'categories': categories, 'products': products})


class ProductDetailView(CategoryDetailMixin, DetailView):

    CT_MODEL_MODEL_CLASS = {
        'notebook': Notebook,
        'smartphone': SmartPhone,
    }

    def dispatch(self, request, *args, **kwargs):
        self.model = self.CT_MODEL_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'product'
    template_name = 'mainapp/product_detail.html'
    slug_url_kwarg = 'slug'


class CategoryDetailView(CategoryDetailMixin, DetailView):
    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'mainapp/category_detail.html'
    slug_url_kwarg = 'slug'
