from django.core.paginator import (Paginator, EmptyPage, PageNotAnInteger)


class GenericPaginator(object):
    """
    Custom dinamic paginations for all views bassed in `generic.ListView`

    1. app/views.py
    context_data['page_range'] = GenericPaginator(
                                    self.get_queryset(),
                                    self.paginate_by,
                                    self.request.GET.get('page')
                                ).get_page_range()

    2. app/templates/name.html
    {% block pagination %}
        {% if is_paginated %}{# `is_paginated` is default bassed in `generic.ListView` #}
        <p class="all-paginate">
          <i>Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}.</i>
        </p>
        <ul class="pagination" style="margin-top:5px;">
          <li {% if not page_obj.has_previous %}class="disabled"{% endif %}>
             <a {% if page_obj.has_previous %}href="?page={{ page_obj.previous_page_number }}" aria-label="Previous" {% endif %}>
                <span aria-hidden="true">&laquo;</span></a>
           </li>
           <li><a href="?page=1">First</a></li>
          {% for linkpage in page_range %}
              {% ifequal linkpage page_obj.number %}
                 <li class="active">
                   <a>{{ page_obj.number }}<span class="sr-only">(current)</span></a>
                 </li>
              {% else %}
                 <li><a href="?page={{ linkpage }}">{{ linkpage }}</a></li>
              {% endifequal %}
          {% endfor %}
          <li><a href="?page={{ page_obj.paginator.num_pages }}">Last</a></li>
          <li {% if not page_obj.has_next %}class="disabled"{% endif %}>
             <a {% if page_obj.has_next %}href="?page={{ page_obj.next_page_number }}" aria-label="Next" {% endif %}>
                <span aria-hidden="true">&raquo;</span></a>
           </li>
        </ul>
        {% endif %}
    {% endblock %}{# end block pagination #}
    """

    def __init__(self, queryset, numb_pages, request_page):
        # egg: models.Video.objects.published()
        self.queryset = queryset

        # egg: int 6 `is number per page`. or from param: `paginate_by` in `generic.ListView`.
        self.numb_pages = numb_pages

        # egg: self.request.GET.get('page')
        self.request_page = request_page

    def get_page_range(self):
        paginator = Paginator(self.queryset, self.numb_pages)
        page = self.request_page
        try:
            tutorials = paginator.page(page)
        except PageNotAnInteger:
            tutorials = paginator.page(1)
        except EmptyPage:
            tutorials = paginator.page(paginator.num_pages)

        index = tutorials.number - 1
        limit = 5  # limit for show range left and right of number pages
        max_index = len(paginator.page_range)
        start_index = index - limit if index >= limit else 0
        end_index = index + limit if index <= max_index - limit else max_index

        # When you return this, you will getting error
        # `page_range TypeError: sequence index must be integer, not 'slice'`.
        # Because now in django changelog, use `xrange`, and not `range`.
        # See this tickets: https://code.djangoproject.com/ticket/23140
        # >>> page_range  = paginator.page_range[start_index:end_index]
        page_range = list(paginator.page_range)[start_index:end_index]
        return page_range
