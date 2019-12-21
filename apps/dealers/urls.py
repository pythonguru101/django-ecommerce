# encoding: utf-8
from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', CityListView.as_view(), name='dealers'),
    url(r'^(?P<slug>[\-\w]+)$', CityView.as_view(), name="dealers-city"),
]