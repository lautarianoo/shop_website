from django import forms
from mainapp.models import Category

class NewCategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = '__all__'
