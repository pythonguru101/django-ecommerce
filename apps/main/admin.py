# encoding: utf-8
from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin as FlatPageAdminOld

from apps.main.forms import PageAdminForm
from apps.main.models import *


class PageAdmin(FlatPageAdminOld):
    adminfiles_fields = ['content']
    form = PageAdminForm
    list_display = (
        'title',
        'url',
        'sort',
        'is_active',
    )
    list_editable = (
        'sort',
        'is_active',
    )
    fieldsets = (
        (None, {
            'fields': (
                'url',
                'title',
                'content',
                'template_name',
                'sites',
            )
        }),
        ('Meta', {
            'fields': (
                'meta_title',
                'meta_keywords',
                'meta_description',
            )
        }),
    )


admin.site.unregister(FlatPage)
admin.site.register(Page, PageAdmin)
