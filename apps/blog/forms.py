#encoding: utf-8
from django import forms
from markdownx.widgets import MarkdownxWidget

from .models import Post

class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'text': MarkdownxWidget(),
        }
