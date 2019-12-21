# encoding: utf-8
from django.db import models
from django.utils.translation import ugettext as _
from apps.core.models import MetaPage
from django.urls import reverse, reverse_lazy

class City(models.Model):

    class Meta:
        ordering = ('sort',)
        verbose_name = _(u'город')
        verbose_name_plural = _(u'города')
        
    name = models.CharField(_(u'город'), blank=False, max_length=80)
    slug = models.SlugField(_(u'метка'))
    sort = models.PositiveSmallIntegerField(_(u'сортировка'), default=1)
    
    def __unicode__(self):
        return self.name


    def get_absolute_url(self):
        return reverse('dealers-city', kwargs={'slug': self.slug})



class Dealer(models.Model):

    class Meta:
        ordering = ['city']
        verbose_name = _(u'диллер') 
        verbose_name_plural = _(u'диллеры')

    city = models.ForeignKey(City, verbose_name=_(u'город'), 
                                related_name='dealers', on_delete=models.CASCADE)
    name = models.CharField(_(u'наименование'), blank=False, max_length=80)
    site = models.URLField(_(u'Сайт'), blank=True)
    
    def __unicode__(self):
        return self.name


class Shop(models.Model):

    class Meta:
        ordering = ['dealer']
        verbose_name = _(u'магазин') 
        verbose_name_plural = _(u'магазины')

    dealer = models.ForeignKey(Dealer, verbose_name=_(u'диллер'),
                                related_name='shops', on_delete=models.CASCADE)
    name = models.CharField(_(u'наименование'), blank=True, max_length=80)
    address = models.CharField(_(u'адрес'), blank=True, max_length=200)
    metro = models.CharField(_(u'метро'), blank=True, max_length=80)
    phone = models.CharField(_(u'телефон'), blank=True, max_length=200)
    description = models.TextField(_(u'описание'), blank=True)
    
    def __unicode__(self):
        return self.name if self.name else "-"
