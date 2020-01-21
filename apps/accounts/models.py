# encoding: utf-8
import datetime
import random
import re
from hashlib import sha1 as sha_constructor

from django.conf import settings
from django.db import models
from django.template.loader import render_to_string
from django.contrib.sites.models import Site

from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


def expiration_date():
    today = datetime.datetime.now()
    delta = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
    return today + delta


class ProfileRegistrationManager(models.Manager):
    def activate_user(self, activation_key):
        sha1_re = re.compile('^[a-f0-9]{40}$')
        if sha1_re.search(activation_key):

            try:
                profile = self.get(activation_key=activation_key)
            except self.model.DoesNotExist:
                return False

            if not profile.is_expired() and not profile.is_confirmed:
                user = profile.user
                user.is_active = True
                user.save()

                profile.is_confirmed = True
                profile.save()
                return user

    def regenerate(self, user):
        try:
            reg = self.get(user=user)
        except ProfileRegistration.DoesNotExist:
            return False

        salt = sha_constructor(str(random.random())).hexdigest()
        username = user.username

        # if isinstance(username, unicode):
        #     username = username.encode('utf-8')
        activation_key = sha_constructor(salt + username).hexdigest()

        user.is_active = False
        user.save()

        reg.activation_key = activation_key
        reg.is_confirmed = False
        reg.expired_at = expiration_date()
        reg.send_regenerated_email()
        return reg.save()

    def create_registration(self, user):
        salt = sha_constructor(str(random.random()).encode('utf-8')).hexdigest()
        username = user.username
        # if isinstance(username, unicode):
        #     username = username.encode('utf-8')
        activation_key = sha_constructor((salt + username).encode('utf-8')).hexdigest()
        return self.create(user=user, activation_key=activation_key)


class ProfileRegistration(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name=_(u'пользователь'), on_delete=models.CASCADE)
    activation_key = models.CharField(_(u'ключ для активации'), blank=False,
                                      max_length=40)
    is_confirmed = models.BooleanField(_(u'активирован'), default=False)
    expired_at = models.DateTimeField(_(u'истекает'), blank=True,
                                      default=expiration_date)

    objects = ProfileRegistrationManager()

    class Meta:
        verbose_name = _(u'Регистрация')
        verbose_name_plural = _(u'Регистрация на сайте')

    def __unicode__(self):
        return _(u'Регистрация')

    def __notify_user(self, *args, **kwargs):
        ctx_dict = kwargs['context']
        subject = kwargs['subject']
        message = render_to_string(kwargs['template'], ctx_dict)
        return self.user.email_user(subject, message,
                                    settings.DEFAULT_FROM_EMAIL)

    def is_expired(self):
        return datetime.datetime.now() >= self.expired_at

    is_expired.boolean = True

    def send_regenerated_email(self):
        site = Site.objects.get_current()
        return self.__notify_user(
            context={
                'activation_key': self.activation_key,
                'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                'site': site,
            },
            subject=u"Восстановление пароля",
            template='email/forgot_email.txt'
        )

    def send_activation_email(self):
        site = Site.objects.get_current()
        return self.__notify_user(
            context={
                'site': site,
                'activation_key': self.activation_key,
                'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS
            },
            subject=u"Регистрация на сайте",
            template='email/activation_email.txt'
        )


class City(models.Model):
    class Meta:
        verbose_name = _(u'город')
        verbose_name_plural = _(u'города')

    name = models.CharField(_(u'город'), unique=True, blank=False,
                            max_length=80)

    def __unicode__(self):
        return self.name.encode('utf-8')


class Profile(models.Model):
    class Meta:
        verbose_name = _(u'Профиль')
        verbose_name_plural = _(u'Профиль')

    GENDER_CHOICES = (
        (1, _(u'муж')),
        (2, _(u'жен')),
    )
    GENDER_CHOICES_DEFAULT = 1

    user = models.OneToOneField(User, primary_key=True, verbose_name=_(u'пользователь'), on_delete=models.CASCADE)
    city = models.ForeignKey(City, blank=True, null=True, verbose_name=_(u'город'), on_delete=models.CASCADE)
    phone = models.CharField(_(u'телефон'), blank=True, max_length=80)
    birthdate = models.DateField(_(u'дата рождения'), blank=True, null=True)
    gender = models.PositiveIntegerField(_(u'пол'), blank=False,
                                         choices=GENDER_CHOICES,
                                         default=GENDER_CHOICES_DEFAULT)

    def __unicode__(self):
        user = self.user
        return u"%s %s [%s]" % (user.first_name, user.last_name, user.email)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        reg = ProfileRegistration.objects.create_registration(instance)
        reg.send_activation_email()
