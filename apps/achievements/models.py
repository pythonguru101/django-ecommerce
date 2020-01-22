# encoding: utf-8
import datetime
from django.db import models
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToCover, ResizeToFill, ResizeToFit, \
    ResizeCanvas, Anchor

from apps.shop.models import Product
from apps.utils import upload_to


class Category(models.Model):
    """Категория соревнований"""

    name = models.CharField(_(u'название'), blank=False, max_length=80)
    description = models.TextField(_(u'описание'), blank=True)
    slug = models.SlugField(_(u'Слаг'), unique=True)
    sort = models.PositiveSmallIntegerField(_(u'сортировка'), default=1)
    is_active = models.BooleanField(_(u'вкл/выкл'), default=True)

    class Meta:
        verbose_name = _(u'тип соревнования')
        verbose_name_plural = _(u'типы соревнований')

    def __unicode__(self):
        return self.name

    def records_by_date(self):
        records = self.records.all()

    # @models.permalink
    def get_absolute_url(self):
        return reverse('achievements-category', kwargs={'slug': self.slug})


class RecordManager(models.Manager):
    def approved(self):
        """только одобренные админом"""
        return self.filter(is_confirmed=True)

    def pending(self):
        """только ожидающие"""
        return self.filter(is_confirmed=False)


class Record(models.Model):
    user = models.ForeignKey(User, verbose_name=_(u'рекордсмен'),
                             related_name='records', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name=_(u'категория'),
                                 related_name='records', on_delete=models.CASCADE)
    powerball = models.ForeignKey(Product, verbose_name=_(u'модель'),
                                  related_name='records', blank=True, null=True, on_delete=models.CASCADE)
    value = models.IntegerField(_(u'скорость вращения(пользователь)'),
                                blank=False, null=False)
    is_confirmed = models.BooleanField(_(u'подтверждён'), default=True)
    comment = models.TextField(_(u'комментарий'), blank=True)
    created_at = models.DateTimeField(_(u'дата'), blank=False, editable=False,
                                      default=datetime.datetime.now)
    approved_at = models.DateTimeField(_(u'дата подтверждения'), blank=True,
                                       null=True,
                                       editable=False)

    objects = RecordManager()

    class Meta:
        verbose_name = _(u'рекорд')
        verbose_name_plural = _(u'рекорды')
        ordering = ['-created_at']

    def __unicode__(self):
        return "%s %s" % (self.value, self.created_at.strftime('%Y.%m.%d'))

    # @models.permalink
    def get_absolute_url(self):
        return reverse('achievements-record', kwargs={'category_slug': self.category.slug, 'id': self.id})


class RecordProof(models.Model):
    record = models.ForeignKey(Record, verbose_name=_(u'рекорд'),
                               related_name='proofs', on_delete=models.CASCADE)
    image = models.ImageField(_(u'изображение'),
                              upload_to=upload_to('achievements'))

    image_photo = ImageSpecField(source='image',
                                 processors=[ResizeToCover(580, 580),
                                             ResizeCanvas(580, 580,
                                                          anchor=Anchor.CENTER)],
                                 format='JPEG',
                                 options={'quality': 90})

    class Meta:
        verbose_name = _(u'картинка с рекордом')
        verbose_name_plural = _(u'картинка с рекордами')
