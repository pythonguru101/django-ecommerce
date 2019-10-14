# encoding: utf-8
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from apps.banners.models import *
from apps.banners.forms import *


class PolyBannerAdmin(admin.ModelAdmin):
    def response_change(self, request, obj):
        orig = super(PolyBannerAdmin, self).response_change(request, obj)
        return redirect(reverse('admin:banners_banner_changelist'))

    def response_add(self, request, obj, post_url_continue='../%s/'):
        orig = super(PolyBannerAdmin, self).response_add(request, obj, 
                        post_url_continue)
        return redirect(reverse('admin:banners_banner_changelist'))


class BannerTextAdmin(PolyBannerAdmin):
    def get_model_perms(self, request):
        return {}


class BannerImageAdmin(PolyBannerAdmin):
    def get_model_perms(self, request):
        return {}
    

class BannerProductAdmin(PolyBannerAdmin):
    def get_model_perms(self, request):
        return {}
    

class BannerAdmin(PolyBannerAdmin):
    
    def has_add_permission(self, request):
        return False
    
    def get_form(self, request, obj=None, **kwargs):
        if isinstance(obj, BannerText):
            return BannerTextAdminForm
        elif isinstance(obj, BannerProduct):
            return BannerProductAdminForm
        elif isinstance(obj, BannerImage):
            return BannerImageAdminForm
        else:
            return super(BannerAdmin, self).get_form(request, obj, **kwargs)
    
    def changelist_view(self, request, extra_context=None):
        tr = super(BannerAdmin, self).changelist_view(request, extra_context)
        return tr
    
    def change_view(self, request, object_id, form_url = '', extra_context=None):
        # extra_context['osm_data'] = self.get_osm_info()
        return super(BannerAdmin, self).change_view(request, object_id, extra_context=extra_context)

    list_display = (
        'name',
        'is_active',
        'sort',
    )
    list_editable = ('sort', )


admin.site.register(Banner, BannerAdmin)
admin.site.register(BannerProduct, BannerProductAdmin)
admin.site.register(BannerText, BannerTextAdmin)
admin.site.register(BannerImage, BannerImageAdmin)
