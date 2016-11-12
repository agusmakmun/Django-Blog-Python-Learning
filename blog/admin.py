from django.contrib import admin
from django import forms
from django.db.models import TextField
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import ugettext_lazy as _
from django.utils.text import capfirst

# Integrating the model to can import and export the data via admin dashboard.
# See this docs: https://goo.gl/QR3Qqp
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from suit.widgets import AutosizedTextarea
from blog.models import *


class AuthorResource(resources.ModelResource):

    class Meta:
        model = Author


class AuthorAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = AuthorResource
    list_display = ('user', 'website', 'about')
    search_fields = ['user__username', 'user__email', 'about']
    list_filter = ['user__is_active', 'user__is_staff', 'user__is_superuser']


class TagResource(resources.ModelResource):

    class Meta:
        model = Tag


class TagAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = TagResource
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


class TagAdminForm(forms.ModelForm):
    meta_description = forms.CharField(
        required=False,
        widget=AutosizedTextarea(
            attrs={'rows': 3, 'class': 'input-xlarge'}))

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name=_('Tags'),
            is_stacked=False
        )
    )

    class Meta:
        model = Post
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TagAdminForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['tags'].initial = self.instance.tags.all()

    def save(self, commit=True):
        post = super(TagAdminForm, self).save(commit=False)
        if commit:
            post.save()

        if post.pk:
            post.tags = self.cleaned_data['tags']
            self.save_m2m()
        return post


class PostResource(resources.ModelResource):

    class Meta:
        model = Post


class PostAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = PostResource
    form = TagAdminForm
    list_display = ('title', 'author', 'created', 'modified', 'publish')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'description', 'author__user__username']
    list_filter = ['publish', 'author__user__username', 'created']
    list_per_page = 20


class PageResource(resources.ModelResource):

    class Meta:
        model = Page


class PageAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = PageResource
    list_display = ('title', 'author', 'created', 'modified', 'publish')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'description', 'author__user__username']
    list_filter = ['publish', 'author__user__username', 'created']
    list_per_page = 20


class GalleryResource(resources.ModelResource):

    class Meta:
        model = Gallery


class GalleryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = GalleryResource
    list_display = ('check_if_image', 'title', 'created', 'modified')
    search_fields = ['title']
    list_filter = ['created']
    list_per_page = 20


class VisitorResource(resources.ModelResource):

    class Meta:
        model = Visitor


class VisitorAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = VisitorResource
    list_display = ('post', 'ip', 'created', 'modified')


admin.site.register(Author, AuthorAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Visitor, VisitorAdmin)
