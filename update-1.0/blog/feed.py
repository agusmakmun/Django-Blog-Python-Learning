from django.contrib.syndication.views import Feed
from .models import Entry

class LatestPosts(Feed):
    title = "Q Blog"
    link = "/feed/"
    description = "Latest Posts of Q"

    def items(self):
        return Entry.objects.published()[:5]
