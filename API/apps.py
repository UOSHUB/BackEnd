from django.apps import AppConfig
from .services import start_grades_checking


class APIConfig(AppConfig):
    name = "API"

    # # When app is ready
    def ready(self):
        # Run grade checking thread
        start_grades_checking()
