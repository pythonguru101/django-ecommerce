from django.conf import settings
from django.conf.urls import include, url

from django.http import HttpResponseRedirect
from django.views.decorators.cache import cache_page
from django.contrib.sitemaps import views as sitemaps_views
from django.contrib import admin

from apps.main.views import Page404View, RootView, yandex_market_view
from apps.main.views import SitemapShop, RootSitemap
from apps.blog.views import SitemapBlog, BlogFeed, powerball_redirect
from apps.achievements.views import SitemapRecordCategory, SitemapRecord


admin.site.site_header = 'Powerballs Dashboard'
admin.site.site_title = 'Powerballs'

sitemaps = {
    '': RootSitemap,
    'shop': SitemapShop,
    'blog': SitemapBlog,
    'leaugue': SitemapRecordCategory,
    'records': SitemapRecord,
}

cache_time = 60 * 60 * 24


js_info_dict = {
    'packages': ('django.contrib.admin', ),
}

urlpatterns = [
    # url(r'^admin/jsi18n/$', 'django.views.i18n.javascript_catalog',
    #     js_info_dict),
    url(r'^$', RootView.as_view(), name="root"),
    url(r'^admin/', admin.site.urls),
    url(r'^markdownx/', include('markdownx.urls')),

    url(r'^shop/', include('apps.shop.urls')),
    url(r'^users/', include('apps.accounts.urls')),
    url(r'^market.yml$', yandex_market_view),

    url(r'^404.html', Page404View.as_view()),

    url(r'^ordernow/', lambda x: HttpResponseRedirect('/')),
    url(r'^archives', lambda x: HttpResponseRedirect('/blog/')),
    url(r'^blog/', include('apps.blog.urls')),
    url(r'^dealers/', include('apps.dealers.urls')),
    url(r'^achievements/', include('apps.achievements.urls')),
    url(r'^feed/$', BlogFeed(), name='feed'),
    url(r'^(?P<slug>[\-\w]+)/$', powerball_redirect),
    url(r'^archives/(?P<slug>[\-\w]+)/$', powerball_redirect),

    url(r'^sitemap.xml$', cache_page(cache_time)(sitemaps_views.sitemap),
        {'sitemaps': sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$', cache_page(cache_time)(sitemaps_views.sitemap),
        {'sitemaps': sitemaps}),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
