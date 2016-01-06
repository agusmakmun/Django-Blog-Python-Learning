from django.shortcuts import render
from django.views import generic
from . import models
from django.http import HttpResponse

import datetime
from django.core.exceptions import ObjectDoesNotExist

class BlogIndex(generic.ListView):
    queryset = models.Entry.objects.published()
    template_name = "home.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context_data = super(BlogIndex, self).get_context_data(**kwargs)
        alltags = models.Tag.objects.all()
        queryset = models.Entry.objects.published()
        context_data['alltags'] = alltags
        context_data['recent_posts'] = queryset[:5] #limitation for recent posts
        return context_data

class BlogDetail(generic.DetailView):
    model = models.Entry
    template_name = "post.html"

    def get_client_ip(self):
        ip = self.request.META.get("HTTP_X_FORWARDED_FOR", None)
        if ip:
            ip = ip.split(", ")[0]
        else:
            ip = self.request.META.get("REMOTE_ADDR", "")
        return ip

    def tracking_hit_post(self):
        entry = self.model.objects.get(pk=self.object.id)
        try:
        	models.Entry_Views.objects.get(entry=entry, ip=self.get_client_ip(), session=self.request.session.session_key)
        except ObjectDoesNotExist:
                view = models.Entry_Views(entry=entry, 
                			  ip=self.request.META['REMOTE_ADDR'],
                			  created=datetime.datetime.now(),
                			  session=self.request.session.session_key)
                view.save()
	    return models.Entry_Views.objects.filter(entry=entry).count()
	
    def get_context_data(self, **kwargs):
    	context_data = super(BlogDetail, self).get_context_data(**kwargs)
    	related_entries = models.Entry.objects.filter(
    		tags__in=list(self.object.tags.all())
    		).exclude(id=self.object.id)
        queryset = models.Entry.objects.published()
        alltags = models.Tag.objects.all()

        context_data['get_client_ip'] = self.get_client_ip
        context_data['tracking_hit_post'] = self.tracking_hit_post()
        context_data['alltags'] = alltags
        context_data['count_tags'] = related_entries.count
    	context_data['related_entries'] = related_entries[:5] #limitation for post
        context_data['recent_posts'] = queryset[:5] #limitation for recent posts
    	return context_data

class PageDetail(generic.DetailView):
    model = models.Page
    template_name = "pages.html"
