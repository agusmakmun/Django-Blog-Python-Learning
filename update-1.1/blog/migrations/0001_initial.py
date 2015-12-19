# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('avatar', models.ImageField(help_text=b'Upload Image for Avatar', null=True, upload_to=b'gallery', blank=True)),
                ('about', ckeditor.fields.RichTextField()),
                ('email', models.EmailField(max_length=200, unique=True, null=True, blank=True)),
                ('website', models.URLField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'Author Detail',
                'verbose_name_plural': 'Author',
            },
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('cover', models.ImageField(null=True, upload_to=b'covers', blank=True)),
                ('body', ckeditor.fields.RichTextField()),
                ('slug', models.SlugField(unique=True, max_length=200)),
                ('keywords', models.CharField(max_length=200, null=True, blank=True)),
                ('publish', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(to='blog.Author')),
            ],
            options={
                'ordering': ['-created'],
                'verbose_name': 'Blog Entry',
                'verbose_name_plural': 'Blog Entries',
            },
        ),
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(help_text=b'Type title of file or image', max_length=200)),
                ('image_upload', models.ImageField(help_text=b'Please Choice only One Field, Image or Files', null=True, upload_to=b'gallery', blank=True)),
                ('file_upload', models.FileField(help_text=b'Please Choice only One Field, Image or Files', null=True, upload_to=b'files', blank=True)),
            ],
            options={
                'ordering': ['-created'],
                'verbose_name': 'Gallery Entry',
                'verbose_name_plural': 'Gallery and Files',
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('body', ckeditor.fields.RichTextField()),
                ('slug', models.SlugField(unique=True, max_length=200)),
                ('publish', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(to='blog.Author')),
            ],
            options={
                'ordering': ['-created'],
                'verbose_name': 'Blog Page',
                'verbose_name_plural': 'Blog Pages',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='entry',
            name='tags',
            field=models.ManyToManyField(to='blog.Tag'),
        ),
    ]
