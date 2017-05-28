from django.http import HttpResponse
import os


# Create your views here.
def layout(request):
    return HttpResponse(open(os.path.dirname(__file__) + '/static/layout.html').read())
