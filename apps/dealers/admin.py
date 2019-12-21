# encoding: utf-8
from django.utils.translation import ugettext as _
from django.contrib import admin

from .models import *

class CityAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('name',) 
    }
    list_display = (
        'name',
        'slug',
        'sort',
    )
    list_editable = (
        'sort',
    )

class DealerAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'city',
        'site',
    )
    list_filter = (
        'city',
    )
    
class ShopAdmin(admin.ModelAdmin):
    list_filter = (
        'dealer',
    )
    list_display = (
        'get_full_name',
        'dealer',
        'get_city',
    )
    
    def get_full_name(self, inst):
        return inst
    get_full_name.short_description = _(u'наименование')
    
    def get_city(self, inst):
        return inst.dealer.city
    get_city.admin_order_field = 'dealer__city'
    get_city.short_description = _(u'город')
    
admin.site.register(City, CityAdmin)
admin.site.register(Dealer, DealerAdmin)
admin.site.register(Shop, ShopAdmin)