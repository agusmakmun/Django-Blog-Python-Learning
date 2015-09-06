from django.shortcuts import render, redirect
from django.http import HttpResponse
from blog.forms import ContactForm

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from blog.models import Entry, Tag

def home(request):
    return render(request, 'blog/base.html', {
		'site_name': 'python.web.id',
		'title':'Python Learning',
		'content': 'Django Blog Python Learning',
		})

def about(request):
	return render(request, 'about.html', {
		'site_name': 'python.web.id',
		'title':'About - Python Learning'
		}) 

def resource(request):
    return render(request, 'resource.html', {
        'site_name': 'python.web.id',
        'title':'Resource - Python Learning'
        })

from django.shortcuts import get_object_or_404

def my_sitemap(request):
    all_entry = Entry.objects.all()

    return render(request, 'sitemap.html', {
        'site_name': 'python.web.id',
        'title':'Sitemap - Python Learning',
        'all_entry':all_entry
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
                send_mail(subject, message, from_email, ['summon.agus2@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('contact')
            #return HttpResponse('Thank you for your message.')
    return render(request, "contact.html", {'form': form})


from django.template import loader, Context
from django.db.models import Q

def search(request):
    query = request.GET['q']
    t = loader.get_template('result.html')
    results = Entry.objects.filter(Q(title__icontains=query) | Q(body__icontains=query) | Q(keywords__icontains=query))#.order_by('created')
    paginator = Paginator(results, 10) #show 10 articles per page
    page = request.GET.get('page')
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)
    index = results.number - 1
    limit = 5 #limit for show range left and right of number pages
    max_index = len(paginator.page_range)
    start_index = index - limit if index >= limit else 0
    end_index = index + limit if index <= max_index - limit else max_index
    page_range = paginator.page_range[start_index:end_index]
    
    c = Context({ 'query': query, 'results':results, 'page_range': page_range, })
    return HttpResponse(t.render(c))

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def displayAllArticlesUnderTage(request, tag_slug):
    #Entry.objects.filter(~Q(id=1))
    t = loader.get_template('all_tags.html')
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
    limit = 5 #limit for show range left and right of number pages
    max_index = len(paginator.page_range)
    start_index = index - limit if index >= limit else 0
    end_index = index + limit if index <= max_index - limit else max_index
    page_range = paginator.page_range[start_index:end_index]

    c = Context({ "articles" : articles_list, "tag_slug" : tag_slug, 'page_range': page_range,})
    return HttpResponse(t.render(c))


from django.template import RequestContext

def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response

def handler500(request):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response
