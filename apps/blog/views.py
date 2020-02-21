# encoding: utf-8
import markdown
from django.contrib.sitemaps import Sitemap
from django.contrib.syndication.views import Feed
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.views.generic import ListView, DetailView

from apps.main.models import Page
from .models import Post


def powerball_redirect(request, slug):
    try:
        page = Page.objects.get(url="/%s/" % slug)
        tpl = page.template_name or 'flatpages/default.html'
        return render_to_response(tpl, {
            'flatpage': page
        }, context_instance=RequestContext(request))

    except Page.DoesNotExist:
        try:
            post = get_object_or_404(Post, slug=slug)
            return redirect('blog-post',
                            year=post.publish_date.year,
                            month=post.publish_date.strftime("%m"),
                            day=post.publish_date.strftime("%d"),
                            slug=post.slug)
        except ValueError:
            raise Http404


class PostListView(ListView):
    context_object_name = 'posts'
    queryset = Post.objects.published_posts()
    paginate_by = 10
    page = 1


class PostView(DetailView):
    context_object_name = 'post'
    model = Post


class SitemapBlog(Sitemap):
    priority = 0.5

    def items(self):
        return Post.objects.published_posts()

    def changefreq(self, inst):
        return "daily"


class BlogFeed(Feed):
    title = _(u"Блог Powerball.ru")
    link = "/feed/"
    description = "powerball.ru blog"

    def items(self):
        return Post.objects.published_posts()[:15]

    def item_title(self, item):
        return item.title

    def author_name(self, item):
        return "powerball.ru"

    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.publish_date

    def item_description(self, item):
        try:
            html = item.text.split('#more')[0]
        except IndexError:
            html = item.text
        return markdown.markdown(html)
