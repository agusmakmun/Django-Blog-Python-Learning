from django.contrib import admin
from django import forms
from django.db.models import TextField
from ckeditor.widgets import CKEditorWidget
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import ugettext_lazy as _
from django.utils.text import capfirst
from blog.models import *

class TagAdminForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(), 
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name=_('Tags'),
            is_stacked=False
            )
        )

    class Meta:
        model = Entry
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TagAdminForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['tags'].initial = self.instance.tags.all()

    def save(self, commit=True):
        entry = super(TagAdminForm, self).save(commit=False)
        if commit:
            entry.save()

        if entry.pk:
            entry.tags = self.cleaned_data['tags']
            self.save_m2m()
        return entry


class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "website", "about")

class EntryAdmin(admin.ModelAdmin):
    form = TagAdminForm
    list_display = ("title", "author", "created", "visit_on_site")
    prepopulated_fields = {"slug": ("title",)}
    search_fields=['title', 'body']
    list_filter = ['author__name', 'created']
    list_per_page = 20
    formfield_overrides = {TextField: {'widget': CKEditorWidget}}
    fieldsets = (
            ('', {
                'fields': (
                            'title', 'slug', 'cover',
                            ('author', 'publish'),
                            'keywords', 'tags', 'body'),
            }),
        )
        
class GalleryAdmin(admin.ModelAdmin):
    list_display = ("file_type", "title", "get_absolute_url", "created")
    search_fields= ['title']
    list_filter = ['created']
    list_per_page = 20
    formfield_overrides = {TextField: {'widget': CKEditorWidget}}

class PageAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created", "visit_on_site") #"status", 
    prepopulated_fields = {"slug": ("title",)}
    search_fields=['title', 'body']
    list_filter = ['author__name', 'created']
    list_per_page = 20
    formfield_overrides = {TextField: {'widget': CKEditorWidget}}
    fieldsets = (
            ('', {
                'fields': (
                            'title', 'slug',
                            ('author', 'publish'),
                            'body'),
            }),
        )

class TagAdmin(admin.ModelAdmin):
    list_per_page = 10

class Entry_Views_Admin(admin.ModelAdmin):
    list_display = ("entry", "ip", "session", "created")
    list_per_page = 20


admin.site.register(Author, AuthorAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Entry_Views, Entry_Views_Admin)
