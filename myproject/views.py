from django.shortcuts import render_to_response
from django.template import RequestContext

def handler400(request):
    response = render_to_response('error_page.html', {'title': '400 Bad Request', 'message': '400'},
                                  context_instance=RequestContext(request, {'message': '400'}))
    response.status_code = 400
    return response

def handler403(request):
    response = render_to_response('error_page.html', {'title': '403 Permission Denied', 'message': '403'},
                                  context_instance=RequestContext(request, {'message': '403'}))
    response.status_code = 403
    return response

def handler404(request):
    response = render_to_response('error_page.html', {'title': '404 Not Found', 'message': '404'},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response

def handler500(request):
    response = render_to_response('error_page.html', {'title': '500 Server Error', 'message': '500'},
                                  context_instance=RequestContext(request, {'message': '500'}))
    response.status_code = 500
    return response