from django.db import models
from django.utils.translation import ugettext as _


class MetaPage(models.Model):
    meta_title = models.CharField(_(u'Заголовок'), blank=True,
                                  max_length=200)
    meta_keywords = models.CharField(_(u'Ключевые слова'), blank=True,
                                     max_length=300)
    meta_description = models.TextField(_(u'Описание'), blank=True)

    class Meta:
        abstract = True
