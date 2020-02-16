# encoding: utf-8
from django import forms
from markdownx.widgets import MarkdownxWidget

from apps.banners.models import BannerText, BannerProduct, BannerImage


class BannerTextAdminForm(forms.ModelForm):
    class Meta:
        model = BannerText
        fields = '__all__'
        widgets = {
            'text': MarkdownxWidget(),
        }


class BannerProductAdminForm(forms.ModelForm):
    class Meta:
        model = BannerProduct
        fields = '__all__'
        widgets = {
            'text': MarkdownxWidget(),
        }


class BannerImageAdminForm(forms.ModelForm):
    class Meta:
        model = BannerImage
        fields = '__all__'
        widgets = {
            'text': forms.Textarea(attrs={'rows': '20', 'cols': '80'})
        }
