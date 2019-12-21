from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.sitemaps import Sitemap
from django.views.generic import TemplateView
from django.contrib.sites.models import Site

from apps.shop.models import Product, Category, ShippingType
from apps.shop.views import ProductListView


def yandex_market_view(request):
    site = Site.objects.get_current()
    categories = Category.objects.filter(is_active=True)

    try:
        shipping = ShippingType.objects.filter(is_active=True)[0]
    except IndexError:
        shipping = None

    context = RequestContext(request, {
        'site': site,
        'categories': categories,
        'shipping': shipping,
        'offers': Product.objects.all(),
    })
    template = loader.get_template('market.yml')
    return HttpResponse(template.render(context).encode('cp1251'), 
                        content_type='text/xml; charset=windows-1251')
    

class RootView(ProductListView):
    pass


class SitemapShop(Sitemap):
    priority = 0.5

    def items(self):
        return Product.objects.filter(is_active=True)
        
    def changefreq(self, inst):
        return "daily"


class RootSitemap(Sitemap):
    location = "/"
    changefreq = "daily"
    priority = 1

    def items(self):
        return [self]


class Page404View(TemplateView):
    template_name = '404.html'
