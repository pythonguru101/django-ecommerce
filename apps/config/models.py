# encoding: utf-8
from django.db import models
from django.utils.translation import ugettext as _


class ConfigAbstractManager(models.Manager):
    def get_config(self):
        try:
            return self.get(pk=1)
        except self.model.DoesNotExist:
            return {}


class ConfigAbstract(models.Model):
    text_main_bot = models.TextField(_(u'текст на главной внизу'), blank=True)
    phone = models.CharField(_(u'номер телефона'), max_length=32, blank=True)
    email = models.EmailField(_(u'email'), blank=True)
    title_page = models.CharField(_(u'заголовок страницы'), max_length=140,
                                  blank=True)
    meta_keywords = models.CharField(_(u'meta keywords'), max_length=200,
                                     blank=True)
    meta_description = models.TextField(_(u'meta description'), blank=True)
    yandex_verification = models.CharField(_(u'Yandex Verification'),
                                           max_length=100, blank=True)

    yml_name = models.CharField(_(u'YML: name'), max_length=250)
    yml_email = models.EmailField(_(u'YML: email'))
    yml_company = models.CharField(_(u'YML: company'), max_length=250)

    objects = ConfigAbstractManager()

    class Meta:
        abstract = True
        verbose_name = _(u'настройки')
        verbose_name_plural = _(u'настройки')

    def __unicode__(self):
        return u'настройки'

    def save(self, *args, **kwargs):
        self.pk = 1
        return super(ConfigAbstract, self).save(*args, **kwargs)


class ConfigManagerManager(models.Manager):
    def get_emails(self):
        return [m['email'] for m in self.values('email')]


class Config(ConfigAbstract):
    title_blog = models.CharField(_(u'заголовок блога'), max_length=140,
                                  blank=True)
    facebook_app_id = models.CharField(_(u'FaceBook App ID'), max_length=100,
                                       blank=True)
    afrek_id = models.CharField(_(u'Партнёрка afrek.ru'), max_length=100,
                                blank=True)


class ConfigManager(models.Model):
    config = models.ForeignKey(Config,
                               verbose_name=_(u'менеджер'), on_delete=models.CASCADE)
    name = models.CharField(_(u'имя'), max_length=100)
    email = models.EmailField(_(u'email'))

    objects = ConfigManagerManager()

    class Meta:
        verbose_name = _(u'менеджер')
        verbose_name_plural = _(u'менеджеры')

    def __unicode__(self):
        return "%s <%s>" % (self.name, self.email)
