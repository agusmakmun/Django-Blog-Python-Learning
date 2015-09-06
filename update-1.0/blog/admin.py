from django.contrib import admin
from . import models

from django_markdown.admin import MarkdownModelAdmin, MarkdownInlineAdmin
from django_markdown.widgets import AdminMarkdownWidget
from django.db.models import TextField

class AuthorAdmin(MarkdownModelAdmin):
    list_display = ("name", "email", "website", "about")
    prepopulated_fields = {"name": ("name",)}
    # Next line is a workaround for Python 2.x
    formfield_overrides = {TextField: {'widget': AdminMarkdownWidget}}

class EntryAdmin(MarkdownModelAdmin):
    list_display = ("title", "author", "created", "visit_on_site") #"status", 
    prepopulated_fields = {"slug": ("title",)}
    # Next line is a workaround for Python 2.x
    #actions = [make_published]
    search_fields=['title', 'body']
    list_filter = ['author__name', 'created']
    list_per_page = 10
    formfield_overrides = {TextField: {'widget': AdminMarkdownWidget}}
    class Media:
    	css = {
    		"all": ("admin/my-custom-admin/mycustom-admin.css",)
    		}
    	js = ("admin/my-custom-admin/my_js.js",)

class GalleryAdmin(MarkdownModelAdmin):
    list_display = ("file_type", "title", "get_absolute_url", "created")
    prepopulated_fields = {"title": ("title",)}
    # Next line is a workaround for Python 2.x
    search_fields= ['title']
    list_filter = ['created']
    list_per_page = 5
    formfield_overrides = {TextField: {'widget': AdminMarkdownWidget}}

class PageAdmin(MarkdownModelAdmin):
    list_display = ("title", "author", "created", "visit_on_site") #"status", 
    prepopulated_fields = {"title": ("title",)}
    search_fields=['title', 'body']
    list_filter = ['author__name', 'created']
    list_per_page = 10
    formfield_overrides = {TextField: {'widget': AdminMarkdownWidget}}
    class Media:
        css = {
            "all": ("admin/my-custom-admin/mycustom-admin.css",)
            }
        js = ("admin/my-custom-admin/my_js.js",)

admin.site.register(models.Author, AuthorAdmin)
admin.site.register(models.Entry, EntryAdmin)
admin.site.register(models.Gallery, GalleryAdmin)
admin.site.register(models.Page, PageAdmin)
admin.site.register(models.Tag)
