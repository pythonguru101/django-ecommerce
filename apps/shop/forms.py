import re

from django import forms
from django.utils.translation import ugettext as _
from markdownx.widgets import MarkdownxWidget

from apps.shop.models import Product, ShippingType, Category
from .plugshop.forms import OrderForm as PlugshopOrderForm


class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'short_description': MarkdownxWidget(),
            'description': MarkdownxWidget(),
        }


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'short_description': MarkdownxWidget(),
            'description': MarkdownxWidget(),
        }


class OrderForm(PlugshopOrderForm):
    shipping_type = forms.ModelChoiceField(empty_label=None,
                                           queryset=ShippingType.objects.filter(is_active=True))
    name = forms.CharField(required=True, error_messages={
        'required': _(u'Укажите имя')
    })
    email = forms.EmailField(required=True, error_messages={
        'required': _(u'Укажите email')
    })
    phone = forms.CharField(required=True, error_messages={
        'required': _(u'Укажите телефон')
    })

    def __require(self, name, error):
        value = self.cleaned_data.get(name, None)
        if len(value) == 0:
            self.errors[name] = [error]

    def clean_name(self):
        name = self.cleaned_data.get('name').strip().split()
        shipping_type = self.cleaned_data.get('shipping_type')
        if shipping_type.require_zip_code and len(name) < 3:
            raise forms.ValidationError(_(u'Введите фамилию имя и отчество'))

        if len(name):
            self.cleaned_data['last_name'] = name[0]
            self.cleaned_data['first_name'] = " ".join(name[1:])
        else:
            raise forms.ValidationError(_(u'Введите имя'))

        return " ".join(name)

    def clean(self):
        cleaned_data = self.cleaned_data
        shipping_type = cleaned_data.get('shipping_type')

        if shipping_type:
            if shipping_type.require_address:
                self.__require('address', _(u'Не указан адрес доставки'))
            if shipping_type.require_zip_code:
                self.__require('zip_code', _(u'Не указан индекс'))
                self.__require('city', _(u'Не указан город'))

                zip_code = self.cleaned_data.get('zip_code', None)
                if re.search(r'^\d{6}$', zip_code) is None:
                    self.errors['zip_code'] = [_(u'Индекс состоит из 6 цифр')]
        return cleaned_data
