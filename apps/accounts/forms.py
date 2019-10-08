# encoding: utf-8
import re
from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class PasswordForm(forms.Form):
    
    password1 = forms.CharField(widget=forms.PasswordInput, error_messages={
                                    'required': _(u'Введите пароль')
                                })
    password2 = forms.CharField(widget=forms.PasswordInput, error_messages={
                                    'required': _(u'Пароли не совпадают')
                                })

    def clean_password1(self):
        pswd1 = self.cleaned_data.get('password1')
        r = re.compile('^[a-zA-Z0-9\_\-]+$')
        if not r.match(pswd1):
            raise forms.ValidationError(_(u'Пароль может содержать только латинские буквы, цифры и знаки «_» и «-»'))
            
        if len(pswd1) < 4 or len(pswd1) > 32:
            raise forms.ValidationError(_(u'Длина пароля от 4 до 32 символов'))
        return pswd1

    def clean_password2(self):
        pswd1 = self.cleaned_data.get('password1')
        pswd2 = self.cleaned_data.get('password2')

        if pswd1 != pswd2:
            raise forms.ValidationError(_(u'Пароли не совпадают'))
        return pswd2


class UserForm(UserCreationForm):
    email = forms.EmailField(required=True, label=_(u'Email'))
    first_name = forms.CharField(required=True, label=_(u'Имя'))
    last_name = forms.CharField(required=True, label=_(u'Фамилия'))

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', )

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = False
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["email"]

        if commit:
            user.save()
        return user
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            User.objects.get(email=email)
            raise forms.ValidationError(_(u'Пользователь с таким логином уже зарегестрирован'))
        except User.DoesNotExist:
            return email