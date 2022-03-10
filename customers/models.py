from django.contrib.auth import get_user_model
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, AnonymousUser
from django.db import models

User = get_user_model()

class CustomerManager(BaseUserManager):

    def create_user(self, email, username, password=None):

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
    date_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone

    def save(self, *args, **kwargs):
        if not self.phone:
            self.phone = '+000 000 00 00'
        super().save(*args, **kwargs)

    @property
    def is_verify(self):
        if self.status == 2:
            return True
        return False

    @property
    def is_anonymous(self):
        if self.status == 0:
            return True
        return False

    @property
    def is_noverify(self):
        if self.status == 1:
            return True
        return False

class Customer(BaseUser):

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    orders = models.ManyToManyField('mainapp.Order', verbose_name='Заказы покупателя', related_name='related_customer', blank=True)

    def __str__(self):
        return self.phone

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class CompanyUser(BaseUser):

    title = models.CharField(verbose_name='Название компании', max_length=100)
    owner = models.ForeignKey(Customer,
                              on_delete=models.SET_NULL,
                              null=True, blank=True)
    products = models.ManyToManyField('mainapp.Product', verbose_name='Продукты компании',
                                      blank=True,
                                      related_name='business')
    avatar = models.ImageField()
    verify = models.BooleanField(default=False)
    rating = models.FloatField(verbose_name='Рейтинг', default=1.1)

    def __str__(self):
        return

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