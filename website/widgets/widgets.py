from django.template.loader import get_template

from .utils import widget


def buienradar_widget():
    return get_template("widgets/buienradar_widget.html").render()


widget.add_widget(buienradar_widget, takes_context=False, width=0)
