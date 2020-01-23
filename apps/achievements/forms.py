# encoding: utf-8
from django import forms
from django.utils.translation import ugettext as _
from markdownx.widgets import MarkdownxWidget

from .models import Record, Category, RecordProof
from apps.shop.models import Product


class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        exclude = (
            'user',
            'is_confirmed',
        )

    powerball = forms.ModelChoiceField(empty_label=None,
                                       queryset=Product.objects.filter(is_active=True))
    category = forms.ModelChoiceField(empty_label=None,
                                      queryset=Category.objects.filter(is_active=True))
    name = forms.CharField(required=True, error_messages={
        'required': _(u'Укажите имя')
    })
    email = forms.EmailField(required=True, error_messages={
        'required': _(u'Укажите email')
    })
    image = forms.FileField(required=True, error_messages={
        'required': _(u'Приложите фото')
    })

    def clean_name(self):
        name = self.cleaned_data.get('name').strip().split()
        shipping_type = self.cleaned_data.get('shipping_type')

        if len(name):
            self.cleaned_data['first_name'] = name[0]
            self.cleaned_data['last_name'] = " ".join(name[1:])
        else:
            raise forms.ValidationError(_(u'Введите имя'))

        return " ".join(name)
