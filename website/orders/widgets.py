from django.template.loader import get_template

from widgets.utils import widget


def active_venues_widget(context):
    venue = context["venue"]



widget.add_widget(active_venues_widget, takes_context=True, width=0)
