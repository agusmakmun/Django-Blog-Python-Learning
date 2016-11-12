### v.3.8
* Fixed trending posts by week.
* Removed pkg-resources

### v.3.7
* Added feature blog post json format: `<post_url>/?format=json`

```
curl -X GET \
  -H "Accept: application/json" \
  https://python.web.id/blog/django-redirect-http-to-https/?format=json
```

* Update for fixed draft post

### v.3.6
* Added feature auto backup to the json file
* Added feature highlight pre
* Fixed draft post
* Fixed typo, sidebar, detail, css, or else

### v.3.5
* Implement Standard [PEP8](https://www.python.org/dev/peps/pep-0008/) for Python.
* Implement CBV (Class Bassed View).
* Migrated from Python 2.7 to [Python 3.5](https://docs.python.org/3/)
* Migrated from Djagno 1.8 to [Django 1.10](https://docs.djangoproject.com/en/1.10/)
* Migrated [Django wp-admin](https://github.com/barszczmm/django-wpadmin) to [Django suit](https://github.com/darklow/django-suit).
* Migrated [Django Ckeditor](https://github.com/django-ckeditor/django-ckeditor) to [Django Redactor](https://github.com/douglasmiranda/django-wysiwyg-redactor).
* Added [Django nocaptcha recaptcha](https://github.com/ImaginaryLandscape/django-nocaptcha-recaptcha) for contact form.
* Added Page for tranding posts by visitor.
* Added Feature export and import using [Django Import Export](https://github.com/django-import-export/django-import-export)
* Changed Gallery Upload to only once attachment field.
* Added custom template for Error page, Maintenance mode, and much more...

### v.3.4

* Fixed MultipleObjectsReturned

### v.3.3

* Fix locate of handlers

### v.3.2

* Fix handling error 400, 403, 404, 500

### v.3.1

* Fixed typo

### v.3.0

* Fixed DEV-OPS and Markdown.

### v.2.1.1

* adding new feature for output post with json format (example: https://python.web.id/json-posts/48/, docs: https://python.web.id/blog/new-feature-output-post-json-format-django-blog-python-learning-v211/)

* adding Simple Django HIT Counter (docs: https://python.web.id/blog/how-build-simple-django-hit-counter/)

* modified RSS syndication (docs: https://python.web.id/blog/building-an-rss-feed-for-your-django-content/)
