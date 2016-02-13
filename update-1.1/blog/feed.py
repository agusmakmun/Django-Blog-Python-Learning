from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed
from django.core.urlresolvers import reverse
from .models import Entry

class CorrectMimeTypeFeed(Rss201rev2Feed):
	mime_type = 'application/xml'
    
class LatestPosts(Feed):
	feed_type = CorrectMimeTypeFeed
	
	title = "Feed Blog Posts"
	link = "/feed/"
	description = "Latest Feed Blog Posts"

	def author_name(self):
		return "Summon Agus"
        
	def items(self):
		return Entry.objects.published()[:10]

	def item_title(self, item):
		return item.title

	def item_description(self, item):
		return item.body

	def item_author_name(self, item):
		return item.author
        
	def item_link(self, item):
		return reverse('entry_detail', args=[item.slug])
	
	def item_pubdate(self, item):
		return item.modified
