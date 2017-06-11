from django.http import HttpResponse, HttpResponseRedirect
import os


# Returns the front-end template 'layout.html' (without Django template rendering)
def layout(request):
    return HttpResponse(open(os.path.dirname(__file__) + '/static/layout.html').read())


# Redirects requests of static files from /<filename> (root url) to /static/<filename>
def static_files(request, filename):
    return HttpResponseRedirect('/static/' + filename)
