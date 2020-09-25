from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from widgets import utils


class DashboardView(TemplateView):
    """Dashboard view."""

    template_name = "widgets/dashboard.html"

    def get(self, request, **kwargs):
        venue = kwargs.get("venue")
        applied_widgets = []
        context = {"request": request, "venue": venue}
        for key, value in utils.widget.get_widgets().items():
            # Create an emtpy unnamed object
            rendered_html = type('', (), {})()
            if value.takes_context:
                rendered_html.html = value(context)
            else:
                rendered_html.html = value()
            rendered_html.width = value.width
            applied_widgets.append(rendered_html)

        return render(request, self.template_name, {"widgets": applied_widgets})
