import datetime
from django.db.models import Q
from django.views import generic
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.template import loader, Context, RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.models import Entry, Tag, Author, Page
from blog.forms import ContactForm

class BlogIndex(generic.ListView):
    queryset = Entry.objects.published()
    template_name = "blog/blog_home.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context_data = super(BlogIndex, self).get_context_data(**kwargs)
        alltags = Tag.objects.all()
        queryset = Entry.objects.published()
        context_data['alltags'] = alltags
        context_data['recent_posts'] = queryset[:5] #limitation for recent posts
        return context_data

class BlogDetail(generic.DetailView):
    model = Entry
    template_name = "blog/blog_post.html"

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
            Entry_Views.objects.get(entry=entry, ip=self.get_client_ip(), session=self.request.session.session_key)
        except ObjectDoesNotExist:
            import socket
            dns = str(socket.getfqdn(str(self.get_client_ip()))).split('.')[-1]
            try:
                if int(dns):
                        view = Entry_Views(entry=entry, 
                                    ip=self.request.META['REMOTE_ADDR'],
                                    created=datetime.datetime.now(),
                                    session=self.request.session.session_key)
                        view.save()
                    else: pass
                except ValueError: pass
        except MultipleObjectsReturned: pass
        return Entry_Views.objects.filter(entry=entry).count()

    def get_context_data(self, **kwargs):
        context_data = super(BlogDetail, self).get_context_data(**kwargs)
        related_entries = Entry.objects.filter(
            tags__in=list(self.object.tags.all())
            ).exclude(id=self.object.id)
        queryset = Entry.objects.published()
        alltags = Tag.objects.all()

        context_data['get_client_ip'] = self.get_client_ip
        context_data['tracking_hit_post'] = self.tracking_hit_post()
        context_data['alltags'] = alltags
        context_data['count_tags'] = related_entries.count
        context_data['related_entries'] = related_entries[:5] #limitation for post
        context_data['recent_posts'] = queryset[:5] #limitation for recent posts
        return context_data

class PageDetail(generic.DetailView):
    model = Page
    template_name = "blog/blog_pages.html"

def about(request):
    return render(request, 'blog/blog_about.html', {
        'site_name': 'python.web.id',
        'title':'About - Python Learning'
        })

def resource(request):
    return render(request, 'blog/blog_resource.html', {
        'site_name': 'python.web.id',
        'title':'Resource - Python Learning'
        })

def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['your_email@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('contact')
    return render(request, "blog/blog_contact.html", {'form': form})

def my_sitemap(request):
    t = loader.get_template('blog/blog_sitemap.html')
    all_entry = Entry.objects.all()
    paginator = Paginator(all_entry, 20) #show 10 articles per page
    page = request.GET.get('page')
    try:
        all_entry = paginator.page(page)
    except PageNotAnInteger:
        all_entry = paginator.page(1)
    except EmptyPage:
        all_entry = paginator.page(paginator.num_pages)
    index = all_entry.number - 1
    limit = 5 #limit for show range left and right of number pages
    max_index = len(paginator.page_range)
    start_index = index - limit if index >= limit else 0
    end_index = index + limit if index <= max_index - limit else max_index
    page_range = paginator.page_range[start_index:end_index]
    
    c = Context({'all_entry':all_entry, 'page_range': page_range, })
    return HttpResponse(t.render(c))

def search(request):
    query = request.GET['q']
    t = loader.get_template('blog/blog_search.html')
    results = Entry.objects.filter(
                                    Q(title__icontains=query) | \
                                    Q(body__icontains=query) | \
                                    Q(keywords__icontains=query)\
                                ).order_by('-created').order_by('-id')
    paginator = Paginator(results, 10) #show 10 articles per page
    page = request.GET.get('page')
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)
    index = results.number - 1
    limit = 3 #limit for show range left and right of number pages
    max_index = len(paginator.page_range)
    start_index = index - limit if index >= limit else 0
    end_index = index + limit if index <= max_index - limit else max_index
    page_range = paginator.page_range[start_index:end_index]
    
    c = Context({ 'query': query, 'results':results, 'page_range': page_range, })
    return HttpResponse(t.render(c))

def displayArticleUnderAuthor(request, pk):
    t = loader.get_template('blog/blog_posts_author.html')
    author = Author.objects.get(pk = pk)
    articles = Entry.objects.filter(author = author.id)
    paginator = Paginator(articles, 10) #show 10 articles per page
    page = request.GET.get('page')
    try:
        articles_list = paginator.page(page)
    except PageNotAnInteger:
        articles_list = paginator.page(1)
    except EmptyPage:
        articles_list = paginator.page(paginator.num_pages)
    index = articles_list.number - 1
    limit = 3 #limit for show range left and right of number pages
    max_index = len(paginator.page_range)
    start_index = index - limit if index >= limit else 0
    end_index = index + limit if index <= max_index - limit else max_index
    page_range = paginator.page_range[start_index:end_index]

    c = Context({ "articles_author" : articles_list, "post_author" : pk, 
                  "author_name": author.name, 'page_range': page_range,})
    return HttpResponse(t.render(c))

def displayAllArticlesUnderTage(request, tag_slug):
    t = loader.get_template('blog/blog_tags.html')
    tag = Tag.objects.get(slug = tag_slug)
    articles = Entry.objects.filter(tags = tag.id)
    paginator = Paginator(articles, 10) #show 10 articles per page
    page = request.GET.get('page')
    try:
        articles_list = paginator.page(page)
    except PageNotAnInteger:
        articles_list = paginator.page(1)
    except EmptyPage:
        articles_list = paginator.page(paginator.num_pages)
    index = articles_list.number - 1
    limit = 3 #limit for show range left and right of number pages
    max_index = len(paginator.page_range)
    start_index = index - limit if index >= limit else 0
    end_index = index + limit if index <= max_index - limit else max_index
    page_range = paginator.page_range[start_index:end_index]

    c = Context({ "articles" : articles_list, "tag_slug" : tag_slug, 'page_range': page_range,})
    return HttpResponse(t.render(c))
