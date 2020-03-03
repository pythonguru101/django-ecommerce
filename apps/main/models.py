from django.contrib.flatpages.models import FlatPage
from django.db import models
from django.utils.translation import ugettext as _

from apps.core.models import MetaPage


class Page(FlatPage, MetaPage):
    sort = models.PositiveIntegerField(_(u'сортировка'), default=1)
    is_active = models.BooleanField(_(u'вкл/выкл'), default=True)

    class Meta:
        ordering = ['sort']
        verbose_name = _(u'страница')
        verbose_name_plural = _(u'Страницы')
