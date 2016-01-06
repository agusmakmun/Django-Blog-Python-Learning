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
        filter_dns = ['ad', 'ae', 'af', 'ag', 'ai', 'al', 'am', 'an', 'ao', 'aq', 'ar', 'as', 'at', 'au', 'aw', 
        'az', 'ba', 'bb', 'bd', 'be', 'bf', 'bg', 'bh', 'bi', 'bj', 'bm', 'bn', 'bo', 'br', 'bs', 'bt', 'bv', 
        'bw', 'by', 'bz', 'ca', 'cc', 'cd', 'cf', 'cg', 'ch', 'ci', 'ck', 'cl', 'cm', 'cn', 'co', 'cr', 'cu', 
        'cv', 'cx', 'cy', 'cz', 'de', 'dj', 'dk', 'dm', 'do', 'dz', 'ec', 'ee', 'eg', 'eh', 'er', 'es', 'et', 
        'fi', 'fj', 'fk', 'fm', 'fo', 'fr', 'fx', 'ga', 'gd', 'ge', 'gf', 'gh', 'gi', 'gl', 'gm', 'gn', 'gp', 
        'gq', 'gr', 'gs', 'gt', 'gu', 'gw', 'gy', 'hk', 'hm', 'hn', 'hr', 'ht', 'hu', 'id', 'ie', 'il', 'in', 
        'io', 'iq', 'ir', 'is', 'it', 'jm', 'jo', 'jp', 'ke', 'kg', 'kh', 'ki', 'km', 'kn', 'kp', 'kr', 'kw', 
        'ky', 'kz', 'la', 'lb', 'lc', 'li', 'lk', 'lr', 'ls', 'lt', 'lu', 'lv', 'ly', 'ma', 'mc', 'md', 'mg', 
        'mh', 'mk', 'ml', 'mm', 'mn', 'mo', 'mp', 'mq', 'mr', 'ms', 'mt', 'mu', 'mv', 'mw', 'mx', 'my', 'mz', 
        'na', 'nc', 'ne', 'nf', 'ng', 'ni', 'nl', 'no', 'np', 'nr', 'nu', 'nz', 'om', 'pa', 'pe', 'pf', 'pg', 
        'ph', 'pk', 'pl', 'pm', 'pn', 'pr', 'pt', 'pw', 'py', 'qa', 're', 'ro', 'ru', 'rw', 'sa', 'sb', 'sc', 
        'sd', 'se', 'sg', 'sh', 'si', 'sj', 'sk', 'sl', 'sm', 'sn', 'so', 'sr', 'st', 'sv', 'sy', 'sz', 'tc', 
        'td', 'tf', 'tg', 'th', 'tj', 'tk', 'tm', 'tn', 'to', 'tp', 'tr', 'tt', 'tv', 'tw', 'tz', 'ua', 'ug', 
        'uk', 'um', 'us', 'us', 'uy', 'uz', 'va', 'vc', 've', 'vg', 'vi', 'vn', 'vu', 'wf', 'ws', 'ye', 'yt', 
        'yu', 'za', 'zm', 'zr', 'zw', 'com', 'net', 'org', 'me', 'biz', 'asia', 'ninja', 'club', 'online', 'website', 'site']

        try:
        	models.Entry_Views.objects.get(entry=entry, ip=self.get_client_ip(), session=self.request.session.session_key)
        except ObjectDoesNotExist:
        	import socket
        	dns = socket.getfqdn(str(self.get_client_ip()))
        	if str(dns).split('.')[-1] not in filter_dns:
                	view = models.Entry_Views(entry=entry, 
                			  ip=self.request.META['REMOTE_ADDR'],
                			  created=datetime.datetime.now(),
                			  session=self.request.session.session_key)
                	view.save()
                else: pass
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
