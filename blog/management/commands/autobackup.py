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

                flastbackup = directory_backup + \
                    '/last_backup_date_{}'.format(time.strftime("%d-%m-%Y"))
                with open(flastbackup, 'w') as f:
                    f.write('Just for date info!')
                    f.close()

            authorset = AuthorResource().export()
            backupMixin(authorset, 'author')

            tagset = TagResource().export()
            backupMixin(tagset, 'tag')

            postset = PostResource().export()
            backupMixin(postset, 'post')

            galleryset = GalleryResource().export()
            backupMixin(galleryset, 'gallery')

            visitorset = VisitorResource().export()
            backupMixin(visitorset, 'visitor')

            pageset = PageResource().export()
            backupMixin(pageset, 'page')

            self.stdout.write(self.style.SUCCESS('[+] Successfully backup blog!'))
        else:
            self.stdout.write(self.style.WARNING('[-] Can not backup blog!'))
