from django.conf.urls import include, url

from django.conf import settings
from django.conf.urls.static import static
from . import views, feed

urlpatterns = [
    url(r'^feed/$', feed.LatestPosts(), name="feed"),
    url(r'^$', views.BlogIndex.as_view(), name="index"),
    url(r'^blog/(?P<slug>\S+)/$', views.BlogDetail.as_view(), name="entry_detail"),
    url(r'^page/(?P<slug>\S+)/$', views.PageDetail.as_view(), name="page_detail"),

    #outputing post with json format
    url(r'^json-posts/(?P<pk>\S+)/$', json_format.json_default_posts, name="page_json_default_post"),
]
