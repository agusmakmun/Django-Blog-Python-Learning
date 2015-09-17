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
from .views import resource, my_sitemap, search, displayAllArticlesUnderTage
from .views import displayArticleUnderAuthor

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^markdown/', include("django_markdown.urls")),
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

] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


"""
uncomment this if you work at localhost: +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""
