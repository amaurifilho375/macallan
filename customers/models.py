from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import re

def validate_cpf_digits(cpf: str) -> bool:
    cpf = re.sub(r'\D', '', (cpf or ''))
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    def dv_calc(nums):
        s = 0
        weight = len(nums) + 1
        for n in nums:
            s += int(n) * weight
            weight -= 1
        r = 11 - s % 11
        return r if r < 10 else 0

    n1 = dv_calc(cpf[:9])
    n2 = dv_calc(cpf[:9] + str(n1))
    return cpf[-2:] == f"{n1}{n2}"

class Customer(models.Model):
    REGION_CHOICES = [
        ('AC','AC'),('AL','AL'),('AP','AP'),('AM','AM'),
        ('BA','BA'),('CE','CE'),('DF','DF'),('ES','ES'),
        ('GO','GO'),('MA','MA'),('MT','MT'),('MS','MS'),
        ('MG','MG'),('PA','PA'),('PB','PB'),('PR','PR'),
        ('PE','PE'),('PI','PI'),('RJ','RJ'),('RN','RN'),
        ('RS','RS'),('RO','RO'),('RR','RR'),('SC','SC'),
        ('SP','SP'),('SE','SE'),('TO','TO'),
    ]

    customer_name = models.CharField(_('customer name'), max_length=64)
    customer_email = models.EmailField(_('email'), max_length=64)
    vat_id = models.CharField(_('vat id'), max_length=11)
    phone_number = models.CharField(_('phone number'), max_length=11)
    zipcode = models.CharField(_('zipcode'), max_length=8)
    street = models.CharField(_('street'), max_length=128)
    street_number = models.CharField(_('street number'), max_length=8)
    complement = models.CharField(_('complement'), max_length=128, blank=True)
    district = models.CharField(_('district'), max_length=32)
    city = models.CharField(_('city'), max_length=32)
    region = models.CharField(_('region'), max_length=2, choices=REGION_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.customer_name} <{self.customer_email}>"

    def clean(self):
        if len((self.customer_name or '').strip().split()) < 2:
            raise ValidationError({'customer_name': _('Informe nome completo')})

        vat_clean = re.sub(r'\D', '', (self.vat_id or ''))
        if not validate_cpf_digits(vat_clean):
            raise ValidationError({'vat_id': _('Informe um CPF válido')})

        phone_clean = re.sub(r'\D', '', (self.phone_number or ''))
        if len(phone_clean) not in (10, 11):
            raise ValidationError({'phone_number': _('Informe um telefone válido')})

        zip_clean = re.sub(r'\D', '', (self.zipcode or ''))
        if len(zip_clean) != 8:
            raise ValidationError({'zipcode': _('Informe um CEP válido')})

    def save(self, *args, **kwargs):
        self.vat_id = re.sub(r'\D', '', (self.vat_id or ''))
        self.phone_number = re.sub(r'\D', '', (self.phone_number or ''))
        self.zipcode = re.sub(r'\D', '', (self.zipcode or ''))
        super().save(*args, **kwargs)