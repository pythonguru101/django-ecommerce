# encoding: utf-8
from django.conf.urls import url

from .views import PostListView, PostView

urlpatterns = [
    url(r'^$', PostListView.as_view(), name='blog-list'),
    url(r'^page/(?P<page>\d+)/$', PostListView.as_view(), name='blog-list'),
    url(r'^post/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[\-\w]+)$',
        PostView.as_view(), name="blog-post"),
]