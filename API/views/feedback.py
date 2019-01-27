from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import redirect
from .common import login_required
import requests, os

# Webhook url and id from environment
webhook = 'https://webhook.site/'
hook_id = os.getenv('webhook', 'fe2bee4d-fbf3-41c0-af9f-693158c03096')

# Feedback requests handler
class Feedback(APIView):
    # Redirects to Webhook on GET request
    @staticmethod
    def get(request):
        # Return a redirect response to Webhook URL
        return redirect(f'{webhook}#/{hook_id}')

    # Sends feedback to Webhook on POST request
    @staticmethod
    @login_required()
    def post(request):
        # Return an empty response with whatever status Webhook returned
        return Response(status=requests.post(
            # Send student text feedback to Webhook
            webhook + hook_id, data={'feedback': request.data['feedback']}
        ).status_code)
