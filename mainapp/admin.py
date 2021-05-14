from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import ModelChoiceField, ModelForm
from .models import *
from django.utils.safestring import mark_safe

from PIL import Image

class NotebookAdminForm(ModelForm):

    MIN_SIZE = (400, 400)
    MAX_SIZE = (900, 900)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = mark_safe(f'<span style="color:red;">Загружайте изображения с минимальным форматом {self.MIN_SIZE[0]}x{self.MIN_SIZE[1]}</span>')

    #def clean_image(self):
        #image = self.cleaned_data['image']
        #img = Image.open(image)
        #min_height, min_width = self.MIN_SIZE
        #if img.height < min_height or img.width < min_width:
         #   raise ValidationError('Загруженное изображение меньше допустимого формата 400x400')

        #max_height, max_width = self.MAX_SIZE
        #if img.height > max_height or img.width > max_width:
        #    raise ValidationError('Загруженное изображение больше допустимого формата 900x900')
        #return image

class NotebookAdmin(admin.ModelAdmin):

    form = NotebookAdminForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='laptop'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SmartphoneAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='smartphone'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Category)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(SmartPhone, SmartphoneAdmin)
admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(CartProduct)
