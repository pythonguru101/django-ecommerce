# encoding: utf-8
import datetime

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy

from apps.core.models import MetaPage

STATUS_DRAFT = 1
STATUS_PUBLISHED = 2
STATUS_CHOICES = (
    (STATUS_DRAFT, _(u'Черновик')),
    (STATUS_PUBLISHED, _(u'Опубликован')),
)


class PostManager(models.Manager):
    def published_posts(self):
        return self.filter(status=STATUS_PUBLISHED).order_by('-publish_date')

    def get_last_post(self):
        try:
            return self.filter(
                status=STATUS_PUBLISHED).order_by('-publish_date')[0:1][0]
        except IndexError:
            return None


class Post(MetaPage):
    class Meta:
        ordering = ('-publish_date',)
        verbose_name = _(u'пост')
        verbose_name_plural = _(u'посты')

    objects = PostManager()

    title = models.CharField(_(u'Заголовок'), blank=False, max_length=200)
    text = models.TextField(_(u'Описание'), blank=True)
    slug = models.SlugField(_(u'Слаг'), unique=True)
    status = models.IntegerField(_(u'Статус'), choices=STATUS_CHOICES,
                                 default=STATUS_DRAFT)
    publish_date = models.DateTimeField(_(u'Дата публикации'), blank=True,
                                        default=datetime.datetime.now)

    # @models.permalink
    def get_absolute_url(self):
        return reverse('blog-post', kwargs={'year': self.publish_date.strftime("%Y"),
                                            'month': self.publish_date.strftime("%m"),
                                            'day': self.publish_date.strftime("%d"),
                                            'slug': self.slug,
                                            })

    def __unicode__(self):
        return self.title
