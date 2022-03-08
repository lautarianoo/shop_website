from django.db import models
from mainapp.models import Category, Product

class CategoryFeature(models.Model):

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='features')
    title = models.CharField(max_length=40)
    value = models.CharField(verbose_name='Контент', max_length=50)
    measure = models.CharField(verbose_name='Измеряется', max_length=50, null=True, blank=True)

    def __str__(self):
        return f"Тип - Категория хар. | {self.title}"

class ProductUniqueFeature(models.Model):

    product = models.ForeignKey(Product, verbose_name='Продукт', on_delete=models.CASCADE, related_name='features')
    title = models.CharField(max_length=40)
    value = models.CharField(verbose_name='Контент', max_length=50)
    measure = models.CharField(verbose_name='Измеряется', max_length=50, null=True, blank=True)

    def __str__(self):
        return f"Тип - уникальная хар. | {self.title}"