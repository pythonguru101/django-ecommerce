# encoding: utf-8
import re
import datetime
from urllib.parse import urlparse
from django import template

register = template.Library()


@register.simple_tag
def active_tag(request, patterns, css='selected'):
    """
    usage:
        <a class="url{% active_tag request "default /home/" %}" href="#">url item 1</a>
        #=> <a class="url seleced">url item 1</a>

        <a class="url{% active_tag request "/posts/ /allposts/" "custom-css" %}" href="#">url item 2</a>
        #=> <a class="url custom-css">url item 2</a>
    """
    if "default" in patterns.split() and request.path == '/':
        return " %s" % css
    else:
        return " %s" % css if len([p for p in patterns.split() 
                            if re.search(p, request.path) ]) else ''


@register.simple_tag
def last_in_row(i, cols, css):
    return css if not i % cols else ''


@register.filter
def more(text):
    try:
        return text.split('#more')[0]
    except IndexError:
        return text


@register.filter
def split(str, splitter):
    return str.split(splitter)
    

@register.filter
def url2domain(url):
    site = urlparse(url)
    return site.netloc
    

@register.simple_tag
def delivery_date(now=None, base_hour=14, extra=None):
    if now is None:
        now = datetime.datetime.now()

    week = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
    week_day = now.weekday()
    rules = (
        # если это будний день и время раньше 14:00, 
        (week_day in (0,1,2,3,4) and now.hour < base_hour, 
            u'Ваш заказ может быть отправлен уже сегодня.'),

        # если это воскресенье-четверг и время больше 14:00. 
        (week_day in (6,0,1,2,3) and now.hour >= base_hour, 
            u'Ваш заказ может быть отправлен завтра.'),

        # если время больше 14:00 и это пятница, 
        # либо если это суббота или воскресенье.
        (week_day in (5, 6) or (week_day is 4 and now.hour >= base_hour), 
            u'Ваш заказ может быть отправлен в понедельник.'),
    )
    try:
        rule = [r[1] for r in rules if r[0]][0]
    except IndexError:
        rule = u''
    return rule


@register.inclusion_tag('tags/button.html')
def button(tag, type, label, **kwargs):
    data_attrs = " ".join(['%s="%s"' % (k.replace('_', '-'), v) 
                for k, v in kwargs.items() if k.find('data_') == 0])
    ctx = {
        'type': type,
        'label': label,
        'data_attrs': " %s" % data_attrs,
    }
    return ctx
    

@register.filter
def sort_flatpage(queryset):
    return queryset.exclude(page__is_active=False).order_by('page__sort')