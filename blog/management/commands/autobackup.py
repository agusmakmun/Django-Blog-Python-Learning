import os
import json
import time
from django.core.management.base import BaseCommand, CommandError

from blog.admin import (
    AuthorResource, TagResource, PostResource,
    GalleryResource, VisitorResource, PageResource
)
from blog.models import Post

'''
    Refferences:
        - http://stackoverflow.com/a/11789141/3445802
        - http://stackoverflow.com/a/3287063/6396981
    See alseo:
        - https://docs.djangoproject.com/es/1.9/howto/custom-management-commands/

    *) If you work with `hosting`, you can setup on `Cron Jobs`,
        and setup your time with command:
    source /path/to/yourenv/bin/activate && cd /path/to/yourenv/yourproject && ./manage.py autobackup yes


    *) But, if you work with VPS or SERVER, please following this command bellow:
    $ sudo crontab -e

    # Setup to daily method.
    [minute] [hour] [date] [month] [year]

    59 23 * * * source /path/to/yourenv/bin/activate && cd /path/to/yourenv/yourproject && ./manage.py autobackup yes

'''


class Command(BaseCommand):
    help = 'To backup the blog using django-import-export!'

    def add_arguments(self, parser):
        parser.add_argument(
            'backup',
            help='To backup the blog using django-import-export!'
        )

    def handle(self, *args, **options):
        if options['backup'] == 'yes':

            # Checking directory backup, exist or yet!
            directory_backup = "autobackupjsondb"
            if os.path.isdir(directory_backup) == False:
                os.makedirs(directory_backup)

            def backupMixin(resources_set, fname):
                filepath = '{}/{}.json'.format(
                    directory_backup,
                    fname
                )
                with open(filepath, 'w') as outfile:
                    json.dump(resources_set.json, outfile)

                # returning file size to 'kB' version.
                return int(os.path.getsize(filepath)) / 1000

            authorset = AuthorResource().export()
            fsizeAuthor = backupMixin(authorset, 'author')

            tagset = TagResource().export()
            fsizeTag = backupMixin(tagset, 'tag')

            postset = PostResource().export()
            fsizePost = backupMixin(postset, 'post')

            galleryset = GalleryResource().export()
            fsizeGallery = backupMixin(galleryset, 'gallery')

            visitorset = VisitorResource().export()
            fsizeVisitor = backupMixin(visitorset, 'visitor')

            pageset = PageResource().export()
            fsizePage = backupMixin(pageset, 'page')

            def backupInfo():
                return ''\
                    '-------------------------------\n' \
                    '| Last backup date: {0}\n' \
                    '-------------------------------\n' \
                    '| Author  : {1} kB\n' \
                    '| Tag     : {2} kB\n' \
                    '| Post    : {3} kB\n' \
                    '| Gallery : {4} kB\n' \
                    '| Visitor : {5} kB\n' \
                    '| Page    : {6} kB\n' \
                    '-------------------------------'.format(
                        time.strftime("%d-%m-%Y"),
                        fsizeAuthor, fsizeTag, fsizePost,
                        fsizeGallery, fsizeVisitor, fsizePage
                    )

            finfo = directory_backup + '/backupinfo.txt'
            with open(finfo, 'w') as f:
                f.write(backupInfo())
                f.close()

            self.stdout.write(
                self.style.SUCCESS(
                    backupInfo()
                )
            )
        else:
            self.stdout.write(
                self.style.WARNING('[-] Can not backup blog!')
            )
