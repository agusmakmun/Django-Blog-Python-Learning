from django import template
from blog.models import *

register = template.Library()

'''
   10 popular tags for sidebar.
   Usage for: includes/menus.html

{% load globaltags %}
{% populartags as populartags_list %}
{% for tag in populartags_list %}
  <a href="{% url 'tag_posts_page' slug=tag.slug %}">
    {{ tag.title }} <span class="badge">{{ tag.total }}</span>
  </a>
{% empty %}
  <p>No tags yet!</p>
{% endfor %}
'''


@register.assignment_tag
def populartags():
    tags_queryset = Tag.objects.all()
    mapping = [
        {
            'tag': tag,
            'total': Post.objects.published().filter(tags__slug=tag.slug).count()
        } for tag in tags_queryset
    ]
    mapping.sort(key=lambda x: int(x['total']), reverse=True)
    return mapping[:10]


@register.assignment_tag
def recentposts():
    posts = Post.objects.published()
    return posts[:5]
