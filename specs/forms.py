from django import forms
from mainapp.models import Category
from .models import CategoryFeature

class NewCategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = '__all__'

class NewCategoryFeatureKeyForm(forms.ModelForm):

    class Meta:
        model = CategoryFeature
        fields = '__all__'

