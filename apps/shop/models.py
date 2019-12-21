# encoding: utf-8
import datetime

from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.translation import ugettext as _
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToCover, ResizeToFit, \
    ResizeCanvas, Anchor
from pytils import numeral

from apps.core.models import MetaPage
from apps.shop.templatetags.plugshop import plugshop_currency
from apps.utils import upload_to
from .plugshop.models.category import CategoryAbstract
from .plugshop.models.order import OrderAbstract
from .plugshop.models.order_products import OrderProductsAbstract
from .plugshop.models.product import ProductAbstract
from .plugshop.settings import STATUS_CHOICES_FINISH
from .plugshop.utils import get_categories


class ShippingType(models.Model):

    class Meta:
        verbose_name = _(u'способ доставки')
        verbose_name_plural =  _(u'способы доставки')
        ordering = ('sort',)

    name = models.CharField(_(u'способ доставки'), blank=False, max_length=100)
    price = models.PositiveIntegerField(_(u'цена'), blank=False, default=0)
    require_address = models.BooleanField(_(u'необходимо указать адрес'), 
                                            default=False)
    require_zip_code = models.BooleanField(_(u'необходимо указать индекс'), 
                                            default=False)
    help = models.TextField(_(u'подсказка'), blank=True, null=True)
    sort = models.PositiveSmallIntegerField(_(u'сортировка'), default=1)
    is_active = models.BooleanField(_(u'активен'), default=True)
    
    def has_requirements(self):
        return self.require_address or self.require_zip_code
    
    def __unicode__(self):
        return self.name


class Order(OrderAbstract):
    
    class Meta:
        verbose_name  = _(u'заказ')
        verbose_name_plural = _(u'заказы')
        ordering = ['-created_at']
        
    shipping_type = models.ForeignKey(ShippingType, 
                                        verbose_name=_(u'способ доставки'),
                                        related_name='orders', on_delete=models.CASCADE)
    city = models.CharField(_(u'город'), blank=True, null=True, max_length=80)
    address = models.TextField(_(u'адрес доставки'), blank=True, null=True)
    zip_code = models.CharField(_(u'индекс'), blank=True, null=True, 
                                max_length=24)
    phone = models.CharField(_(u'телефон'), blank=False, max_length=80)
    ip_address = models.CharField(_(u'IP'), blank=True, null=True, max_length=80)
    comment = models.TextField(_(u'комментарий'), blank=True)
    
    def price_without_shipping(self):
        return super(Order, self).price_total()
    
    def price_total(self):
        price = super(Order, self).price_total()
        shipping_price = self.shipping_type.price
        return price + shipping_price


class OrderProducts(OrderProductsAbstract):
    class Meta:
        verbose_name = _('order product')
        verbose_name_plural = _('order product')


class Category(CategoryAbstract):
    short_description = models.TextField(_(u'краткое описание'), blank=True)
    description = models.TextField(_(u'описание'), blank=True)
    is_active = models.BooleanField(_(u'активен'), default=True)
    sort = models.PositiveSmallIntegerField(_(u'сортировка'), default=1)
    
    def get_first_product(self):
        try:
            return self.products.all()[0]
        except IndexError:
            return None
    
    class Meta:
        ordering = ['sort']
        verbose_name  = _(u'категория')
        verbose_name_plural = _(u'категории')

    def __str__(self):
        return self.name


class Product(ProductAbstract, MetaPage):

    class Meta:
        ordering = ('sort', )
        verbose_name  = _(u'товар')
        verbose_name_plural = _(u'товары')
        
    is_active = models.BooleanField(_(u'активен'), default=True)
    short_description = models.TextField(_(u'краткое описание'), blank=True)
    description = models.TextField(_(u'описание'), blank=True)
    sort = models.PositiveSmallIntegerField(_(u'сортировка'), default=1)
    # weight = models.IntegerField(_('weight'), null=True)
    # sku = models.CharField(_('SKU'), null=True, max_length=200)
    
    def get_cover(self):
        coverset = ProductImage.objects.filter(product=self)
        if (len(coverset)):
            return coverset[0]

    def has_video(self):
        return len(ProductVideo.objects.filter(product=self)) > 0
        
    def label_buy(self):
        currency = plugshop_currency(self.price)
        label = numeral.choose_plural(self.price, (u'рубль', u'рубля', u'рублей'))
        return u"Купить за %s %s" % (currency, label)


class Option(models.Model):

    name = models.CharField(_(u'Наименование'), blank=False, max_length=200, 
                            unique=True)
                            
    class Meta:
        verbose_name = _(u'опция')
        verbose_name_plural = _(u'опции для товара')
        
    def __str__(self):
        return self.name


class ProductImage(models.Model):

    product = models.ForeignKey(Product, verbose_name=_(u'товар'),
                                        related_name='images', on_delete=models.CASCADE)
    sort = models.PositiveSmallIntegerField(_(u'сортировка'), default=1)
    image = models.ImageField(_(u'изображение'), 
                              upload_to=upload_to('products'))

    image_admin = ImageSpecField(source='image', 
                                    processors=[ResizeToCover(100, 100)], 
                                    format='JPEG', options={'quality': 90})

    image_banner = ImageSpecField(source='image', 
                                    processors=[ResizeToFit(250, 250),
                                                ResizeCanvas(250, 250, 
                                                        anchor=Anchor.CENTER)], 
                                    format='PNG')
                                
    image_product = ImageSpecField(source='image', 
                                    processors=[ResizeToFit(280, 280),
                                                ResizeCanvas(280, 280, 
                                                    anchor=Anchor.CENTER)], 
                                    format='PNG')
                                
    image_category = ImageSpecField(source='image', 
                                    processors=[ResizeToFit(160, 160),
                                                ResizeCanvas(160, 160, 
                                                        anchor=Anchor.CENTER)], 
                                    format='PNG')
                                
    image_list = ImageSpecField(source='image', 
                                processors=[ResizeToFit(160, 160),
                                            ResizeCanvas(160, 160, 
                                                anchor=Anchor.CENTER)], 
                                 format='PNG')

    image_cart = ImageSpecField(source='image', 
                                processors=[ResizeToFit(86, 86),
                                            ResizeCanvas(86, 86, 
                                                        anchor=Anchor.CENTER)], 
                                format='PNG')

    class Meta:
        verbose_name = _(u'изображение товара')
        verbose_name_plural = _(u'изображения товара')
        ordering = ('sort', )


class ProductVideo(models.Model):
    class Meta:
        verbose_name = _(u'видео для товара')
        verbose_name_plural = _(u'видео для товара')
        ordering = ('sort', )
        
    product = models.ForeignKey(Product, verbose_name=_(u'товар'),
                                        related_name='videos', on_delete=models.CASCADE)
    embeded = models.TextField(_(u'Код для видео'), blank=False)
    sort = models.PositiveSmallIntegerField(_(u'сортировка'), default=1)


class ProductOption(models.Model):
    class Meta:
        ordering = ('sort',)
        verbose_name = _(u'характеристика товара')
        verbose_name_plural = _(u'характеристики товара')
        
    product = models.ForeignKey(Product, verbose_name=_(u'товар'), 
                                        related_name='options', on_delete=models.CASCADE)
    option = models.ForeignKey(Option, verbose_name=_(u'опция'), on_delete=models.CASCADE)
    value = models.CharField(_(u'значение'), blank=False, max_length=200, 
                            default="")
    sort = models.PositiveSmallIntegerField(_(u'сортировка'), default=1)

    def __unicode__(self):
        o = self.option
        return "%s = %s" % (o.name, self.value)
        

@receiver(post_save, sender=Order)
def order_created(sender, instance, created, **kwargs):
    #индекс, страна, город, адрес, фио
    pass

@receiver(pre_save, sender=Order)
def set_delivered(sender, instance, **kwargs):
    if instance.status == STATUS_CHOICES_FINISH:
        instance.delivered_at = datetime.datetime.now()
    else:
        instance.delivered_at = None


@receiver(pre_save, sender=Order)
def generate_number(sender, instance, **kwargs):
    if instance.id is None:
        now = datetime.datetime.now()
        hour_from = datetime.datetime(now.year, now.month, now.day, now.hour)
        hour_till = hour_from + datetime.timedelta(hours=1)

        today_orders = Order.objects.filter(Q(created_at__gte=hour_from),
                                                  Q(created_at__lt=hour_till))

        today_orders_nums = [0]
        for o in today_orders:
            num = str(o.number)[8:]
            try:
                today_orders_nums.append(int(num))
            except ValueError:
                today_orders_nums.append(max(today_orders_nums))

        num = max(today_orders_nums) + 1
        instance.number = u"%s%s" % (now.strftime('%y%m%d%H'), num)

post_save.connect(get_categories, sender=Category)