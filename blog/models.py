from django.db import models
from django.db.models import TextField
from django.core.urlresolvers import reverse
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
import datetime

class EntryQuerySet(models.QuerySet):
    def published(self):
        return self.filter(publish=True)

class Author(models.Model):
    name    = models.CharField(max_length=200)
    avatar  = models.ImageField(upload_to='gallery/%Y/%m/%d', null=True, blank=True, help_text="Upload Image for Avatar")
    about   = models.TextField()
    email   = models.EmailField(max_length=200, blank=True, null=True, unique=True)
    website = models.URLField(max_length=200, blank=True, null=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('author-detail', kwargs={'pk': self.pk})
       
    class Meta:
        verbose_name = "Author Detail"
        verbose_name_plural = "Author"

class Tag(models.Model):
    slug        = models.SlugField(max_length=200, unique=True)

    def __unicode__(self):
        return self.slug

class Entry(models.Model):
    title       = models.CharField(max_length=200)
    cover       = models.ImageField(upload_to='covers/%Y/%m/%d', null=True, blank=True)
    body        = RichTextUploadingField()#RichTextField()
    slug        = models.SlugField(max_length=200, unique=True)
    author      = models.ForeignKey('Author')
    keywords    = models.CharField(max_length=200, null=True, blank=True)
    publish     = models.BooleanField(default=True)
    created     = models.DateTimeField(auto_now_add=True)
    modified    = models.DateTimeField(auto_now=True)
    tags        = models.ManyToManyField('Tag')

    objects = EntryQuerySet.as_manager()

    domain_post = 'https://python.web.id/blog/'

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("entry_detail", kwargs={"slug": self.slug})

    def visit_on_site(self):
        return '<a href="'+self.domain_post+str(self.slug)+'" target="_blank">'+str(self.slug)+'</a>'
    visit_on_site.allow_tags = True

    def json_default_post(self):
        domain = 'https://python.web.id'
        cover_url = 'None'
        try:
            cover_url = domain+str(self.cover.url)
        except:
            cover_url = cover_url

        return dict(
            title = self.title,
            url = domain+"/blog/"+str(self.slug),
            cover =  cover_url,
            author = self.author.name,
            created = self.created.isoformat(),
            modified = self.modified.isoformat(),
            tags = [p.slug for p in self.tags.all()],
            body = self.body
        )

    class Meta:
        verbose_name = "Blog Entry"
        verbose_name_plural = "Blog Entries"
        ordering = ["-created"]

class Gallery(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=200, help_text="Type title of file or image")
    image_upload = models.ImageField(upload_to='gallery/%Y/%m/%d', null=True, blank=True, help_text="Please Choice only One Field, Image or Files")
    file_upload = models.FileField(upload_to='files/%Y/%m/%d', null=True, blank=True, help_text="Please Choice only One Field, Image or Files")

    domain = 'https://python.web.id'

    def file_type(self):
        if self.image_upload:
            return '<img height="40" width="60" src="%s"/>' % self.image_upload.url
        return '<img height="40" width="45" src="/static/asset/icons/file-icon.png"/>'
    file_type.short_description = 'Type'
    file_type.allow_tags = True

    def get_absolute_url(self):
        if self.image_upload:
            return '<a href="'+self.domain+self.image_upload.url+'" target="_blank">'+self.domain+self.image_upload.url+'</a>'
        return '<a href="'+self.domain+self.file_upload.url+'" target="_blank">'+self.domain+self.file_upload.url+'</a>'
    get_absolute_url.short_description = 'Absolute Url'
    get_absolute_url.allow_tags = True

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = "Gallery Entry"
        verbose_name_plural = "Gallery and Files"
        ordering = ["-created"]

class Page(models.Model):
    title = models.CharField(max_length=200)
    body = RichTextUploadingField()#RichTextField()
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey('Author')
    publish = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    domain_post = 'https://python.web.id/page/'

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("page_detail", kwargs={"slug": self.slug})

    def visit_on_site(self):
        return '<a href="'+self.domain_post+str(self.slug)+'" target="_blank">'+str(self.slug)+'</a>'
    visit_on_site.allow_tags = True

    class Meta:
        verbose_name = "Blog Page"
        verbose_name_plural = "Blog Pages"
        ordering = ["-created"]

class Entry_Views(models.Model):
    entry = models.ForeignKey(Entry, related_name='entry_views')
    ip = models.CharField(max_length=40)
    session = models.CharField(max_length=40, null=True)
    created = models.DateTimeField(default=datetime.datetime.now())

    def __unicode__(self):
        return self.entry.title

    class Meta:
        verbose_name_plural = "Entry Views"
        ordering = ["-created"]
