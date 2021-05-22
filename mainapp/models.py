from django.db import models
import sys
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.urls import reverse



#функциональщина
User = get_user_model()

def get_models_for_count(*models_names):
    return [models.Count(model_name) for model_name in models_names]

def get_product_url(obj, viewname):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})

class MinResoluitionError(Exception):
    pass

class MaxResolutionError(Exception):
    pass

class LatestProductsManager:

    @staticmethod
    def get_products_for_mainpage(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.objects.filter(model__in = args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(products, key=lambda x: x.__class__._meta.model_name.starswith(with_respect_to),
                                  reverse=True)
        return products

class LatestProducts:

    objects = LatestProductsManager()

class CategoryManager(models.Manager):

    CATEGORY_NAME_COUNT_NAME = {
        'Ноутбуки': 'notebook__count',
        'Смартфоны': 'smartphone__count',
    }

    def get_queryset(self):
        return super().get_queryset()

    def get_category_for_left_sidebar(self):
        models = get_models_for_count('notebook', 'smartphone')
        qs = list(self.get_queryset().annotate(*models))
        data = [
            dict(name=c.name, url=c.get_absolute_url(), count=getattr(c, self.CATEGORY_NAME_COUNT_NAME[c.name]))
            for c in qs
        ]
        return data


#модели
class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)
    objects = CategoryManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

class Product(models.Model):

    MIN_SIZE = (400, 400)
    MAX_SIZE = (900, 900)

    class Meta:
        abstract = True

    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Наименование продукта')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        image = self.image
        img = Image.open(image)
        new_img = img.convert('RGB')
        resized_new_img = new_img.resize((600, 600), Image.ANTIALIAS)
        filestream = BytesIO()
        resized_new_img.save(filestream, 'JPEG', quality=90)
        filestream.seek(0)
        name = '{}.{}'.format(*self.image.name.split('.'))
        self.image = InMemoryUploadedFile(
            filestream, 'ImageField', name, 'jpeg/image', sys.getsizeof(filestream), None
        )
        super().save(*args, **kwargs)

    def get_model_name(self):
        return self.__class__.__name__.lower()

class Notebook(Product):

    diagonal = models.CharField(max_length=255, verbose_name='Диагональ')
    display =  models.CharField(max_length=255, verbose_name='Тип дисплея')
    processor_freq = models.CharField(max_length=255, verbose_name='Частота процессора')
    ram = models.CharField(max_length=255, verbose_name='Оперативная память')
    videocard = models.CharField(max_length=255, verbose_name='Видеокарта')

    def __str__(self):
        return f"{self.category.name}: {self.title}"

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')



class SmartPhone(Product):

    diagonal = models.CharField(max_length=255, verbose_name='Диагональ')
    display = models.CharField(max_length=255, verbose_name='Тип дисплея')
    resolution = models.CharField(max_length=255, verbose_name='Разрешение')
    accum_volume = models.CharField(max_length=255, verbose_name='Объём батареи')
    ram = models.CharField(max_length=255, verbose_name='Оперативная память')
    sd = models.BooleanField(default=True)
    sd_volume = models.CharField(max_length=255, verbose_name='Макс. объём SD',
                                 null=True, blank=True)
    main_cam_mp = models.CharField(max_length=255, verbose_name='Главная камера')
    frontal_cam_mp = models.CharField(max_length=255, verbose_name='Фронтальная камера')

    def __str__(self):
        return f"{self.category.name}: {self.title}"

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')



class CartProduct(models.Model):

    user = models.ForeignKey('Customer', verbose_name='Юзер', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    quality = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
        return f"Корзина - {self.user}"

    def save(self, *args, **kwargs):
        self.total_price = self.quality * self.content_object.price
        super().save(*args, **kwargs)



class Cart(models.Model):

    owner = models.ForeignKey('Customer', verbose_name='Владелец', on_delete=models.CASCADE, null=True)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0, null=True)
    total_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Общая цена')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        cart_data = self.products.aggregate(models.Sum('total_price'), models.Count('id'), models.Sum('quality'))
        if cart_data.get('total_price__sum'):
            self.total_price = cart_data['total_price__sum']
        else:
            self.total_price = 0
        self.total_products = cart_data['quality__sum'] #cart_data['id__count']
        super().save(*args, **kwargs)


    def __str__(self):
        return f"Корзина пользователя №{self.owner.id}"


class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name='Юзер', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)

    #def __str__(self):
        #return self.user
