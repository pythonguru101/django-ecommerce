# encoding: utf-8
import requests
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from apps.banners.models import Banner
from apps.config.models import ConfigManager
from apps.shop.listeners import add_item, remove_item, order_create_signal
from apps.shop.models import Product, ProductImage, Category
from apps.shop.signals import cart_append, cart_remove, order_create
from .plugshop.views import CartView as PlugshopCartView
from .plugshop.views import CategoryListView as PlusghopCategoryListView
from .plugshop.views import CategoryView as PlusghopCategoryView
from .plugshop.views import OrderCreateView as PlusghopOrderCreateView
from .plugshop.views import OrderView as PlusghopOrderView
from .plugshop.views import ProductListView as PlugshopProductListView
from .plugshop.views import ProductView as PlugshopProductView


def inject_covers(context):
    products = context.get('products', [])
    products_ids = [p.id for p in products]

    images = ProductImage.objects.filter(product__in=products_ids)
    for p in products:
        cover = list(filter(lambda x: x.product_id == p.id, images))
        try:
            setattr(p, 'cover', cover[0])
        except IndexError:
            setattr(p, 'cover', None)
    context.update(products=products)
    return context


def inject_banner(context):
    banners = Banner.objects.filter(is_active=True)
    try:
        banner = banners[0]
    except IndexError:
        banner = None
    context.update(banner=banner)

    return context


class CategoryView(PlusghopCategoryView):

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        products = context['products']
        context['products'] = products.filter(is_active=True)

        context = inject_banner(context)
        context = inject_covers(context)
        return context


class CategoryListView(PlusghopCategoryListView):
    queryset = Category.objects.all().order_by('sort')


class ProductListView(PlugshopProductListView):

    def get_queryset(self):
        return Product.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context = inject_banner(context)
        context = inject_covers(context)
        return context


class CartView(PlugshopCartView):
    def post(self, request, **kwargs):
        return super(CartView, self).post(request, **kwargs)


class ProductView(PlugshopProductView):
    def get_context_data(self, *args, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)
        return context


class OrderCreateView(PlusghopOrderCreateView):
    
    def get_admin_mail_title(self, order):
        return u"Новый заказ на сайте powerball.ru №%s" % order.number
        
    def notify_managers(self, order):
        import csv
        from io import StringIO
        
        addresses = ConfigManager.objects.get_emails()
        if len(addresses):
            fields = (
                ('number', u'номер заказа'),
                ('price', u'цена'),
                ('price_total', u'цена с доставкой'),
                ('address', u'адрес'),
                ('city', u'город'),
                ('zip_code', u'индекс'),
                ('phone', u'телефон'),
                ('first_name', u'имя'),
                ('last_name', u'фамилия'),
                ('email', u'почта'),
                ('date', u'дата'),
            )
            data = {
                'number': order.number, 
                'price': str(order.price_without_shipping()),
                'price_total': str(order.price_total()),
                'address': (order.address or '').encode('utf-8'), 
                'city': (order.city or '').encode('utf-8'),
                'zip_code': (str(order.zip_code) or '').encode('utf-8'), 
                'phone': (order.phone or '').encode('utf-8'), 
                'first_name': (order.user.first_name or '').encode('utf-8'), 
                'last_name': (order.user.last_name or '').encode('utf-8'), 
                'email': order.user.email, 
                'date': order.created_at.isoformat(),
            }
            csv_out = StringIO()
            csv_data = csv.DictWriter(csv_out,  list(zip(*fields))[0])
            csv_data.writerow(dict((k,v.encode('utf-8')) for k,v in fields))
            csv_data.writerow(data)

            cart = self.request.cart
            msg = render_to_string('plugshop/email/order_admin.html', {
                'cart': cart,
                'order': order,
                'total': cart.price_total(),
            })

            # B2Cpl upload
            resp = requests.get('http://is.b2cpl.ru/portal/client_api.ashx', {
                'client': 'test',
                'key': 'test',
                'func': 'upload',
                'file': csv_out.getvalue(),
                'report': 0,
                'stickers': 1
            })
            # if resp.ok:
            #      print("________BTCPL Success________")
            # else:
            #     print("_______BTCPL Failed_______")


            email = EmailMessage(self.get_admin_mail_title(order), msg,
                                    settings.SERVER_EMAIL, addresses)
            email.content_subtype = "html"
            email.attach("order_%s.csv" % order.number, csv_out.getvalue(), 
                        'text/csv')
            email.send()
            csv_out.close()


class OrderView(PlusghopOrderView):
    def get(self, request, **kwargs):
        response = super(OrderView, self).get(request, **kwargs)

        ctx = self.get_context_data(**kwargs)
        order = ctx.get('order', None)

        response.set_signed_cookie('u_o', "%s_%s" % (
                                    order.user.id, order.number))
        return response
    
cart_append.connect(add_item)
cart_remove.connect(remove_item)
order_create.connect(order_create_signal)