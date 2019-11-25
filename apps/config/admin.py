#coding: utf-8
from django.contrib import admin
from apps.config.models import ConfigManager, Config


class ConfigManagerAdminInline(admin.TabularInline):
    model = ConfigManager
    extra = 0


class ConfigAdmin(admin.ModelAdmin):
    inlines = [
        ConfigManagerAdminInline,
    ]

    # def has_add_permission(self, request):
    #     return self.model.objects.count() == 0


admin.site.register(Config, ConfigAdmin)
