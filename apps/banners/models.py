# encoding: utf-8
from django.db import models
from django.utils.translation import ugettext as _
from django.db.models.signals import pre_save
from django.contrib.sites.models import Site

from polymorphic.models import PolymorphicModel
from polymorphic.showfields import ShowFieldContent

from apps.shop.models import Product
from apps.utils import upload_to


class Banner(ShowFieldContent, PolymorphicModel):
    class Meta:
        ordering = ('sort',)
        verbose_name = _(u'банер')
        verbose_name_plural = _(u'банеры')

    name = models.CharField(_(u'имя'), blank=False, max_length=100)
    text = models.TextField(_(u'текст'), blank=True)
    sort = models.PositiveSmallIntegerField(_(u'сортировка'), default=1)
    is_active = models.BooleanField(_(u'вкл/выкл'), default=True)

    def __unicode__(self):
        return self.name


class BannerProduct(Banner):
    class Meta:
        verbose_name = _(u'банер с товаром')
        verbose_name_plural = _(u'банеры с товаром')

    TEMPLATE_CHOICES_DEFAULT = 'banners/product/default.html'
    TEMPLATE_CHOICES = (
        (TEMPLATE_CHOICES_DEFAULT, _(u'Товар по умолчанию')),
    )

    product = models.ForeignKey(Product, verbose_name=_(u'товар'), on_delete=models.CASCADE)
    template = models.CharField(_(u'шаблон'), blank=False, max_length=80,
                                choices=TEMPLATE_CHOICES,
                                default=TEMPLATE_CHOICES_DEFAULT)


class BannerText(Banner):
    class Meta:
        verbose_name = _(u'банер с текстом')
        verbose_name_plural = _(u'банеры с текстом')

    TEMPLATE_CHOICES_DEFAULT = 'banners/text/default.html'
    TEMPLATE_CHOICES = (
        (TEMPLATE_CHOICES_DEFAULT, _(u'Текст по умолчанию')),
    )

    template = models.CharField(_(u'шаблон'), blank=False, max_length=80,
                                choices=TEMPLATE_CHOICES,
                                default=TEMPLATE_CHOICES_DEFAULT)


class BannerImage(Banner):
    class Meta:
        verbose_name = _(u'банер с картинкой')
        verbose_name_plural = _(u'банеры с картинкой')

    TEMPLATE_CHOICES_DEFAULT = 'banners/image/default.html'
    TEMPLATE_CHOICES = (
        (TEMPLATE_CHOICES_DEFAULT, _(u'картинка по умолчанию')),
    )

    template = models.CharField(_(u'шаблон'), blank=False, max_length=80,
                                choices=TEMPLATE_CHOICES,
                                default=TEMPLATE_CHOICES_DEFAULT)
    image = models.ImageField(_(u'изображение'),
                              upload_to=upload_to('banners'))

    def render(self):
        # site = Site.objects.get_current()
        return self.text.replace('{{img}}', self.image.url)


def toggle_banners(sender, instance, **kwargs):
    if instance.is_active:
        Banner.objects.all().update(is_active=False)
        instance.is_active = True


pre_save.connect(toggle_banners, sender=Banner,
                 dispatch_uid="banners.Banner.toggle_banners")
pre_save.connect(toggle_banners, sender=BannerProduct,
                 dispatch_uid="banners.BannerProduct.toggle_banners")
pre_save.connect(toggle_banners, sender=BannerText,
                 dispatch_uid="banners.BannerText.toggle_banners")
pre_save.connect(toggle_banners, sender=BannerImage,
                 dispatch_uid="banners.BannerImage.toggle_banners")
