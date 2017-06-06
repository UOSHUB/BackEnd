from django.http import HttpResponse, HttpResponseRedirect
import os


# Create your views here.
def layout(request):
    return HttpResponse(open(os.path.dirname(__file__) + '/static/layout.html').read())


def static_files(request, filename):
    return HttpResponseRedirect('/static/' + filename)
