# encoding: utf-8
from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', CategoryListView.as_view(), name='achievements-categories'),

    url(r'^new/$', RecordCreateView.as_view(), name='achievements-record-new'),
    url(r'^(?P<slug>[\-\w]+)/new/$', RecordCreateView.as_view(),
        name='achievements-record-cat-new'),

    url(r'^(?P<slug>[\-\w]+)/$', CategoryView.as_view(),
        name='achievements-category'),

    url(r'^(?P<slug>[\-\w]+)/(?P<year>\d{4})/(?P<month>\d{2})/$',
        CategoryView.as_view(),
        name='achievements-category-monthly'),

    url(r'^(?P<category_slug>[\-\w]+)/(?P<id>\d+)$', RecordView.as_view(), name='achievements-record'),
]
