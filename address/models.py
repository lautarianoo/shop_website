from django.db import models
from customers.models import Customer
from django.utils.translation import gettext_lazy as _
from utills.fields import CountrieField

class Address(models.Model):

    customer = models.ForeignKey(Customer, related_name='addresses', on_delete=models.CASCADE,
                                 blank=True, null=True)
    address_1 = models.CharField(max_length=1024,
                                 blank=True, null=True)
    address_2 = models.CharField(max_length=1024,
                                 blank=True, null=True)
    zip_code = models.CharField(max_length=1024, blank=True)
    city = models.CharField(max_length=1024)
    country = CountrieField()

    class Meta:
        verbose_name = _("Shipping address")
        verbose_name_plural = _("Shipping addresses")


