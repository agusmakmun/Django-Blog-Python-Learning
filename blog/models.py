from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from redactor.fields import RedactorField


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Author(models.Model):
    user = models.ForeignKey(User, related_name='author')
    avatar = models.ImageField(upload_to='gallery/avatar/%Y/%m/%d',
                               null=True,
                               blank=True,
                               help_text="Upload your photo for Avatar")
    about = models.TextField()
    website = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('author_posts_page',
                       kwargs={'username': self.user.username})

    class Meta:
        verbose_name = 'Detail Author'
        verbose_name_plural = 'Authors'


class Tag(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.title

    @property
    def get_total_posts(self):
        return Post.objects.filter(tags__pk=self.pk).count()

    class Meta:
        verbose_name = 'Detail Tag'
        verbose_name_plural = 'Tags'


class PostQuerySet(models.QuerySet):

    def published(self):
        return self.filter(publish=True)


class Post(TimeStampedModel):
    author = models.ForeignKey(Author, related_name='author_post')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    cover = models.ImageField(upload_to='gallery/covers/%Y/%m/%d',
                              null=True,
                              blank=True,
                              help_text='Optional cover post')
    description = RedactorField()
    tags = models.ManyToManyField('Tag')
    keywords = models.CharField(max_length=200, null=True, blank=True,
                                help_text='Keywords sparate by comma.')
    meta_description = models.TextField(null=True, blank=True)

    publish = models.BooleanField(default=True)
    objects = PostQuerySet.as_manager()

    def get_absolute_url(self):
        return reverse('detail_post_page', kwargs={'slug': self.slug})

    @property
    def total_visitors(self):
        return Visitor.objects.filter(post__pk=self.pk).count()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Detail Post'
        verbose_name_plural = 'Posts'
        ordering = ["-created"]


class Page(TimeStampedModel):
    author = models.ForeignKey(Author, related_name='author_page')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = RedactorField()
    publish = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    # this will be an error in /admin
    # def get_absolute_url(self):
    #    return reverse("page_detail", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "Detail Page"
        verbose_name_plural = "Pages"
        ordering = ["-created"]


class Gallery(TimeStampedModel):
    title = models.CharField(max_length=200)
    attachment = models.FileField(upload_to='gallery/attachment/%Y/%m/%d')

    def __str__(self):
        return self.title

    def check_if_image(self):
        if self.attachment.name.split('.')[-1].lower() \
                in ['jpg', 'jpeg', 'gif', 'png']:
            return ('<img height="40" width="60" src="%s"/>' % self.attachment.url)
        return ('<img height="40" width="60" src="/static/assets/icons/file-icon.png"/>')
    check_if_image.short_description = 'Attachment'
    check_if_image.allow_tags = True

    class Meta:
        verbose_name = 'Detail Gallery'
        verbose_name_plural = 'Galleries'
        ordering = ['-created']


class Visitor(TimeStampedModel):
    post = models.ForeignKey(Post, related_name='post_visitor')
    ip = models.CharField(max_length=40)

    def __str__(self):
        return self.post.title

    class Meta:
        verbose_name = 'Detail Visitor'
        verbose_name_plural = 'Visitors'
        ordering = ['-created']
