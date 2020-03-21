# -*- coding: utf-8 -*-
from django.utils.deprecation import MiddlewareMixin

from .plugshop.cart import Cart
from .plugshop.settings import REQUEST_NAMESPACE, SESSION_NAMESPACE


class CartMiddleware(MiddlewareMixin):
    def process_request(self, request):
        setattr(request, REQUEST_NAMESPACE, Cart(request, SESSION_NAMESPACE))

    def process_response(self, request, response):
        if hasattr(request, REQUEST_NAMESPACE):
            cart = getattr(request, REQUEST_NAMESPACE)
            cart.save()
        return response
