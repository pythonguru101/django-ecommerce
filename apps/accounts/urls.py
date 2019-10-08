# encoding: utf-8
from django.urls import path, re_path

from apps.accounts.views import ConfirmView


app_name = 'apps.accounts'

urlpatterns = [
    re_path(r'^confirm/(?P<key>\w+)$', ConfirmView.as_view(), name='account-confirm'),

]
