from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from blog.views import *
from blog.feed import LatestPosts

info_dict = {
    'queryset': Post.objects.all(),
    'date_field': 'modified',
}

# Removed url pattern for `slug` to `[\w\-]+` and not `\S+`
# Because it will getting error 404 if use for '/' (homepage) and '/<slug>' (page/else)
# But, makesure the `url page` placed at the bottom from other urls.
# Example:
#   good: r'^(?P<slug>[\w\-]+)/$'
#   bad: r'^(?P<slug>\S+)/$'
# thanks to: http://stackoverflow.com/a/30271379/6396981

urlpatterns = [
    # Handler for Maintenance mode.
    # url(r'^$', TemplateView.as_view(template_name='maintenance.html', content_type='text/html')),

    url(r'^$', HomepageView.as_view(), name='homepage'),
    url(r'^blog/(?P<slug>[\w\-]+)/$', DetailPostView.as_view(), name='detail_post_page'),
    url(r'^search/$', SearchPostsView.as_view(), name='search_posts_page'),
    url(r'^author/(?P<username>[\w\-]+)/$', AuthorPostsView.as_view(), name='author_posts_page'),
    url(r'^tag/(?P<slug>[\w\-]+)/$', TagPostsView.as_view(), name='tag_posts_page'),

    url(r'^feed/$', LatestPosts(), name="feed"),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': {'blog': GenericSitemap(
        info_dict, priority=0.6)}}, name='django.contrib.sitemaps.views.sitemap'),
    url(r'^robots\.txt/$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),

    url(r'^sitemap/$', SitemapView.as_view(), name='sitemap_page'),
    url(r'^contact/$', ContactView.as_view(), name='contact_page'),
    url(r'^trending/$', TrendingPostsView.as_view(), name='trending_posts_page'),
    url(r'^(?P<slug>[\w\-]+)/$', DetailPageView.as_view(), name='detail_page'),
]
