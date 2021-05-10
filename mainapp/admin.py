from django.contrib import admin
from django import forms
from .models import *


class NotebookCategoryChoiceField(forms.ModelChoiceField):
    pass

class NotebookAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return NotebookCategoryChoiceField(Category.objects.filter(slug='laptop'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class SmartphoneCategoryChoiceField(forms.ModelChoiceField):
    pass

class SmartphoneAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return SmartphoneCategoryChoiceField(Category.objects.filter(slug='smartphone'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Category)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(SmartPhone, SmartphoneAdmin)
admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(CartProduct)
