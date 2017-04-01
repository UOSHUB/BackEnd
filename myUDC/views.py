from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .browser import br
from time import time


def index(request):
    if request.method == 'GET' and 'sid' in request.GET and 'pin' in request.GET:
        start = time()
        if br.login(request.GET['sid'], request.GET['pin']):
            return JsonResponse({
                'UserName': br.get_username(),
                'ExecutionTime': round(time() - start, 2)
            })
        return HttpResponse('<h2>Wrong Credentials</h2>')
