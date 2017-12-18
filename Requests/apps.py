from django.apps import AppConfig
from .services import start_grades_checking


class RequestsConfig(AppConfig):
    name = "Requests"

    # When app is ready
    def ready(self):
        # Run grade checking thread
        start_grades_checking()
