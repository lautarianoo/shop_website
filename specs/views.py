from django.shortcuts import render
from django.views import View
from .forms import NewCategoryForm
from django.http import HttpResponseRedirect

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
