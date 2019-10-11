# encoding: utf-8
from django.utils.translation import ugettext as _
from django.contrib import admin
from django.conf import settings
from .models import *

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('name',) 
    }
    list_display = (
        'name',
        'slug',
        'sort',
        'is_active',
    )
    
    list_editable = (
        'sort', 'is_active',
    )

class RecordProofAdminInline(admin.TabularInline):
    model = RecordProof
    extra = 0

class RecordAdmin(admin.ModelAdmin):
    inlines = (
        RecordProofAdminInline,
    )
    list_display = (
        'value',
        'created_at',
        'get_user',
        'is_confirmed',
    )
    date_hierarchy = 'created_at'
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    list_per_page = 30
    
    def get_user(self, inst):
        user = inst.user
        return "%s %s [%s]" % (user.first_name, user.last_name, user.email)
    get_user.short_description = _(u'пользователь')
    
admin.site.register(Category, CategoryAdmin)
admin.site.register(Record, RecordAdmin)