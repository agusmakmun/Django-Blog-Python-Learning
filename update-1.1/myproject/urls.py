"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static
from blog.views import BlogIndex

from django.views.generic import TemplateView

from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from blog.models import Entry
from .views import thanks, contact, about
from .views import resource, my_sitemap, search
from .views import displayAllArticlesUnderTage
from .views import displayArticleUnderAuthor

info_dict = {
    'queryset': Entry.objects.all(),
    'date_field': 'modified',
}

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^', include('blog.urls')),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': {'blog': GenericSitemap(info_dict, priority=0.6)}}, name='django.contrib.sitemaps.views.sitemap'),
    url(r'^robots\.txt/$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    url(r'^about/$', about, name='about'),
    url(r'^resource/$', resource, name='resource'),
    url(r'^sitemap/$', my_sitemap, name='my_sitemap'),
    url(r'^contact/$', contact, name='contact'),
    url(r'^results/$', search, name='search'),
    url(r'^tag/(?P<tag_slug>\S+)/$', displayAllArticlesUnderTage, name="tag_slug"),
    url(r'^author/(?P<pk>\S+)/$', displayArticleUnderAuthor, name="pk"),
] #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)