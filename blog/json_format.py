import json
from blog.models import Entry
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

"""Outputing post to JSON format, with pk/id from post."""
def json_default_posts(request, pk):
    try:
        entry = Entry.objects.get(pk=pk)
        data = entry.json_default_post()
    except ObjectDoesNotExist:
        data = {'error_message':'Object Does NotExist'}

    return HttpResponse(json.dumps(data, indent=4), content_type='application/json')
