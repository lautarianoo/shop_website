from django.shortcuts import render
from django.views import View
from .forms import NewCategoryForm, NewCategoryFeatureKeyForm, NewFeatureForProduct
from django.http import HttpResponseRedirect
from .models import *
from mainapp.models import Product

class BaseSpecView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'specs/product_features.html', {})

class NewCategoryView(View):

    def get(self, request, *args, **kwargs):
        form = NewCategoryForm(request.POST or None)
        return render(request, 'specs/new_category.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = NewCategoryForm(request.POST or None)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/product-specs/')
        return  render(request, 'specs/new_category.html', {'form': form})

class NewFeatureView(View):

    def get(self, request, *args, **kwargs):
        form = NewCategoryFeatureKeyForm(request.POST or None)
        return render(request, 'specs/new_feature.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = NewCategoryFeatureKeyForm(request.POST or None)
        if form.is_valid():
            new_category_featurekey = form.save(commit=False)
            new_category_featurekey.category = form.cleaned_data['category']
            new_category_featurekey.feature_name = form.cleaned_data['feature_name']
            new_category_featurekey.save()
            return HttpResponseRedirect('/product-specs/')
        return  render(request, 'specs/new_category.html', {'form': form})

class NewFeatureProductView(View):

    def get(self, request, *args, **kwargs):
        form = NewFeatureForProduct(request.POST or None)
        return render(request, 'specs/new_feature_product.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = NewFeatureForProduct(request.POST or None)
        if form.is_valid():
            new_feature_product = form.save(commit=False)
            new_feature_product.product = form.cleaned_data['product']
            new_feature_product.feature = form.cleaned_data['feature']
            new_feature_product.save()
            return HttpResponseRedirect('/product-specs/')
        return render(request, 'specs/new_feature_product.html', {'form': form})
