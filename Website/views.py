from django.http import HttpResponse


# Create your views here.
def layout(request):
    return HttpResponse(open('Website/static/layout.html').read())
