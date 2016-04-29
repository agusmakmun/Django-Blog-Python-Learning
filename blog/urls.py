from django.conf.urls import include, url
from . import feed, json_format
from blog.views import *

urlpatterns = [
    url(r'^feed/$', feed.LatestPosts(), name="feed"),
    url(r'^sitemap/$', my_sitemap, name='my_sitemap'),
    url(r'^results/$', search, name='search'),
    url(r'^about/$', about, name='about'),
    url(r'^resource/$', resource, name='resource'),
    url(r'^contact/$', contact, name='contact'),
    
    url(r'^$', BlogIndex.as_view(), name="index"),
    url(r'^blog/(?P<slug>\S+)/$', BlogDetail.as_view(), name="entry_detail"),
    url(r'^page/(?P<slug>\S+)/$', PageDetail.as_view(), name="page_detail"),
    url(r'^json-posts/(?P<pk>\S+)/$', json_format.json_default_posts, name="page_json_default_post"),
    url(r'^tag/(?P<tag_slug>\S+)/$', displayAllArticlesUnderTage, name="tag_page"),
    url(r'^author/(?P<pk>\S+)/$', displayArticleUnderAuthor, name="author_page"),
]
