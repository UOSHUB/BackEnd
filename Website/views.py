from django.http import HttpResponse
from django.template.loader import render_to_string
import os


# Returns the front-end template 'layout.html' after merging css & js includes
def layout(request):
    return HttpResponse(
        # Open '/static/layout.html' as a normal file as read only
        open(os.path.dirname(__file__) + '/static/layout.html').read().replace(
            # Replace the first occurrence of '<!--INCLUDES-->' with Django rendered URLs
            '<!--INCLUDES-->', render_to_string('includes.html'), 1
        )
    )
