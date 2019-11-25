# encoding: utf-8
from django.contrib import admin

from .models import *
from .forms import PostAdminForm

class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    adminfiles_fields = ['description']
    list_display = (
        'title', 
        'status',
        'publish_date',
    )
    fieldsets = (
        (None, {
            'fields': (
                'title',
                'status',
                'slug',
                'publish_date',
                'text',
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
    prepopulated_fields = {
        'slug': ('title',) 
    }
admin.site.register(Post, PostAdmin)