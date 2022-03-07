from django.shortcuts import render
from django.views import View
from .forms import NewCategoryForm, NewCategoryFeatureKeyForm, NewFeatureForProduct
from django.http import HttpResponseRedirect
from .models import *
from mainapp.models import Product
