from django.apps import AppConfig


class WidgetsConfig(AppConfig):
    name = 'widgets'

    def ready(self):
        from widgets import utils
        from widgets import widgets

