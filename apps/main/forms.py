from django import forms
from django.utils.translation import ugettext as _
from django.forms.widgets import Select
from markdownx.widgets import MarkdownxWidget

from apps.main.models import Page

TEMPLATE_CHOICES = (
    ('flatpages/default.html', _(u'Основной')),
)


class PageAdminForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = '__all__'
        widgets = {
            'content': MarkdownxWidget(),
            'template_name': Select(choices=TEMPLATE_CHOICES)
        }