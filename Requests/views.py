from django.http import HttpResponse, JsonResponse
from . import myudc as udc, blackboard as bb, reports as rep


def index(request):
    return HttpResponse('')
