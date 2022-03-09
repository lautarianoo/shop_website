from django.contrib.auth import get_user_model
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, AnonymousUser
from django.db import models
from mainapp.models import Product

User = get_user_model()

class CustomerManager(BaseUserManager):

    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username=None, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            username=username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class BaseUser(AbstractBaseUser):

    class Meta:
        abstract = True

    objects = CustomerManager()

    STATUS = (
        (0, 'Anonymous'),
        (1, 'NoVerify'),
        (2, 'Verify')
    )

    phone = models.CharField(max_length=20, verbose_name='Номер телефона', unique=True, null=True, blank=True)
    email = models.EmailField(verbose_name='Email', unique=True)
    status = models.CharField(choices=STATUS, max_length=50)
    date_reg = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone

    @property
    def is_verify(self):
        if self.status == 2:
            return True
        return False

class Customer(BaseUser):

    #address = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)
    orders = models.ManyToManyField('Order', verbose_name='Заказы покупателя', related_name='related_customer', blank=True)

class CompanyUser(BaseUser):

    title = models.CharField(verbose_name='Название компании', max_length=100)
    products = models.ManyToManyField(Product, verbose_name='Продукты компании', blank=True, related_name='business')
    avatar = models.ImageField()
    verify = models.BooleanField(default=False)
    rating = models.FloatField(verbose_name='Рейтинг', default=1.1)

class VisitingCustomer:

    user = AnonymousUser()

    def __str__(self):
        return 'Visitor'

    @property
    def email(self):
        return ''

    @email.setter
    def email(self, value):
        pass

    @property
    def is_anonymous(self):
        return True

    @property
    def is_authenticated(self):
        return False

    @property
    def is_recognized(self):
        return False

    @property
    def is_guest(self):
        return False

    @property
    def is_registered(self):
        return False

    @property
    def is_visitor(self):
        return True

    def save(self, **kwargs):
        pass