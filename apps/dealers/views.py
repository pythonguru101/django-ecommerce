# encoding: utf-8
from django.http import Http404
from django.views.generic import ListView, DetailView

from .models import City


class CityView(DetailView):
    model = City

    def get_object(self, **kwargs):
        try:
            return super(CityView, self).get_object(**kwargs)
        except AttributeError:
            raise Http404

    def get_context_data(self, **kwargs):
        ctx = super(CityView, self).get_context_data(**kwargs)
        city = ctx.get('city')

        ctx.update(
            dealers=city.dealers.all(),
            city_list=self.model.objects.all()
        )
        return ctx


class CityListView(ListView):
    context_object_name = 'city_list'
    model = City
