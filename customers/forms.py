from django import forms
from .models import Customer
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re

def only_digits(value):
    return re.sub(r'\D', '', value or '')

def validate_cpf_digits(cpf: str) -> bool:
    cpf = re.sub(r'\D', '', cpf or '')
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

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'customer_name', 'customer_email', 'vat_id',
            'phone_number', 'zipcode', 'street', 'street_number',
            'complement', 'district', 'city', 'region'
        ]
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'customer_name', 'placeholder': ''
            }),
            'customer_email': forms.EmailInput(attrs={
                'class': 'form-control', 'id': 'customer_email', 'placeholder': ''
            }),
            
            'vat_id': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'vat', 'placeholder': '000.000.000-00'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'phone', 'placeholder': '(00) 00000-0000',
                'type': 'tel', 'inputmode': 'tel'
            }),
            'zipcode': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'zipcode', 'placeholder': '00000-000'
            }),
            'street': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'street', 'placeholder': ''
            }),
            'street_number': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'street_number', 'placeholder': '', 'maxlength': '8'
            }),
            'complement': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'complement', 'placeholder': ''
            }),
            'district': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'district', 'placeholder': ''
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'city', 'placeholder': ''
            }),
            'region': forms.Select(attrs={
                'class': 'form-control', 'id': 'region'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        big_max = '30'
        for fname in ('vat_id', 'phone_number', 'zipcode'):
            try:
                w = self.fields[fname].widget
                
                w.attrs['maxlength'] = big_max
                
                if fname == 'phone_number':
                    w.attrs.setdefault('type', 'tel')
                    w.attrs.setdefault('inputmode', 'tel')
            except KeyError:
                pass

    def clean_customer_name(self):
        name = self.cleaned_data.get('customer_name', '').strip()
        if len(name.split()) < 2:
            raise forms.ValidationError(_('Informe nome completo'))
        return name

    def clean_customer_email(self):
        email = self.cleaned_data.get('customer_email', '')
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError(_('Informe um e-mail válido'))
        return email

    def clean_vat_id(self):
        vat = only_digits(self.cleaned_data.get('vat_id', ''))
        if not validate_cpf_digits(vat):
            raise forms.ValidationError(_('Informe um CPF válido'))
        return vat

    def clean_phone_number(self):
        phone = only_digits(self.cleaned_data.get('phone_number', ''))
        if len(phone) not in (10, 11):
            raise forms.ValidationError(_('Informe um telefone válido'))
        return phone

    def clean_zipcode(self):
        zipc = only_digits(self.cleaned_data.get('zipcode', ''))
        if len(zipc) != 8:
            raise forms.ValidationError(_('Informe um CEP válido'))
        return zipc