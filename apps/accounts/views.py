# encoding: utf-8

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from apps.accounts.models import ProfileRegistration


class ConfirmView(TemplateView):
    template_name = 'accounts/confirm.html'

    def get_context_data(self, **kwargs):
        ctx = super(ConfirmView, self).get_context_data(**kwargs)

        key = self.kwargs.get('key')
        registration = get_object_or_404(ProfileRegistration, activation_key=key)

        ctx.update(
            registration=registration,
            is_confirmed=True
        )

        if registration.is_confirmed:
            raise Http404
        ProfileRegistration.objects.activate_user(key)
        return ctx
