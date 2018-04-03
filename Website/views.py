from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.template.loader import render_to_string
import os

# Dictionary of abbreviations and their corresponding UOS websites URLs
urls = {
    "udc": "https://uos.sharjah.ac.ae:9050/prod_enUS/twbkwbis.P_WWWLogin",
    "uos": "http://www.sharjah.ac.ae/en/Pages/default.aspx",
    "ms": "https://www.outlook.com/sharjah.ac.ae",
    "bb": "https://elearning.sharjah.ac.ae/",
}


# Redirects to UOS websites by abbreviation
def redirect_to_uos(request, site):
    return HttpResponsePermanentRedirect(urls[site])


# Returns the front-end template "layout.html" after merging css & js includes
def layout(request):
    return HttpResponse(
        # Open "/static/layout.html" as a normal file in read only mode
        open(os.path.dirname(__file__) + "/static/layout.html").read().replace(
            # Replace the first occurrence of "<!--INCLUDES-->" with Django rendered URLs
            "<!--INCLUDES-->", render_to_string("includes.html"), 1
        )
    )
