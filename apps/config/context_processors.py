# encoding: utf-8

from .models import Config

def app_config(request):
    config = Config.objects.get_config()
    return {
        
        'app': config
    }