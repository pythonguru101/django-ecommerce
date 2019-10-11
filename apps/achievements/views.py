# encoding: utf-8

import datetime

from dateutil.relativedelta import relativedelta

from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext as _
from django.views.generic import ListView, DetailView, FormView
from django.db.models import Q, Avg, Count, Max, Min
from django.contrib.auth.models import User
from django.contrib.sitemaps import Sitemap

from .models import Category, Record, RecordProof
from .forms import RecordForm
from apps.accounts.models import Profile, City


class CategoryListView(ListView):
    queryset = Category.objects.filter(is_active=True)
    context_object_name = 'categories'


class CategoryView(DetailView):
    context_object_name = 'category'
    model = Category
    
    def __get_records(self, records):

        profiles = Profile.objects.select_related().filter(
                                    user_id__in=[r.user_id for r in records])

        cities = City.objects.filter(id__in=[p.city_id for p in profiles])
        for r in records:
            try:
                profile = [p for p in profiles if p.user_id == r.user_id][0]
            except IndexError:
                continue

            try:
                city = [c for c in cities if c.id == profile.city_id][0]
                setattr(profile, 'city', city)
            except IndexError:
                continue
        
            setattr(r.user, 'profile', profile)
        return records


    def get_context_data(self, **kwargs):
        ctx = super(CategoryView, self).get_context_data(**kwargs)
        category = ctx.get('category')
        year, month = self.kwargs.get('year'), self.kwargs.get('month')

        try:
            date_from = datetime.date(int(year), int(month), 1)
        except TypeError:
            records_max = category.records.filter(is_confirmed=True).aggregate(
                                    Max('created_at'))

            date_from = records_max['created_at__max']
        try:
            date_till = date_from + relativedelta(months=1)
        except TypeError as e:

            raise Http404

        
        records = category.records.select_related().all().filter(
                        Q(is_confirmed=True),
                        Q(created_at__gte=date_from),
                        Q(created_at__lt=date_till)
                    ).order_by('-value')

        if len(records) == 0:
            raise Http404
        records_prev = category.records.filter(
                            is_confirmed=True,
                            created_at__lt=date_from).aggregate(
                                Max('created_at'))
        records_next = category.records.filter(
                            is_confirmed=True,
                            created_at__gte=date_till).aggregate(
                                Min('created_at'))
        month_str = u"январь февраль март апрель май июнь июль август сентябрь октябрь ноябрь декабрь"
        ctx['records_prev'] = records_prev['created_at__max']
        ctx['records_next'] = records_next['created_at__min']
        ctx['records_date_str'] = " ".join([month_str.split()[date_from.month-1], 
                                        str(date_from.year)])

            # records = ctx.get('category'
            #             ).records.select_related().all().order_by(
            #                 '-value')[0:20]
        ctx['records'] = self.__get_records(records)
        return ctx


class RecordView(DetailView):
    model = Record
    
    def get_object(self):
        record = get_object_or_404(Record, id=self.kwargs.get('id'))
        return record
        
    def get_context_data(self, **kwargs):
        ctx = super(RecordView, self).get_context_data(**kwargs)
        return ctx
    

class RecordCreateView(FormView):
    template_name = 'achievements/record_form.html'
    model = Record
    form_class = RecordForm
    
    def get_context_data(self, **kwargs):
        ctx = super(RecordCreateView, self).get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        if slug:
            category = get_object_or_404(Category, slug=slug)
            ctx.update(category=category)
        return ctx
    
    def form_valid(self, form):
        user, created = User.objects.get_or_create(
            email = form.cleaned_data.get('email')
        )
        if created:
            user.username = form.cleaned_data.get('email')
            user.email = form.cleaned_data.get('email')
            user.first_name = form.cleaned_data.get('first_name', '')
            user.last_name = form.cleaned_data.get('last_name', '')
            user.is_active = False
            user.save()

        record = Record.objects.create(
            user=user,
            category=form.cleaned_data.get('category'),
            powerball=form.cleaned_data.get('powerball.ru'),
            value=form.cleaned_data.get('value'),
            comment=form.cleaned_data.get('comment')
        )
        
        record_proof = RecordProof.objects.create(
            record=record,
            image=form.cleaned_data.get('image')
        )
        return redirect(record.get_absolute_url())


class SitemapRecordCategory(Sitemap):
    priority = 0.5
    
    def items(self):
        return Category.objects.filter(is_active=True)

    def changefreq(self, inst):
        return "monthly"


class SitemapRecord(Sitemap):
    priority = 0.5
    
    def items(self):
        return Record.objects.approved()

    def changefreq(self, inst):
        return "monthly"