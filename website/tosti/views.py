from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView, RedirectView

from tosti.filter import Filter


class IndexView(TemplateView):
    """Index view."""

    template_name = "tosti/index.html"

    def get(self, request, **kwargs):
        """
        GET request for IndexView.

        :param request: the request
        :param kwargs: keyword arguments
        :return: a render of the index page
        """
        return render(request, self.template_name)


class PrivacyView(TemplateView):
    """Privacy policy view."""

    template_name = "tosti/privacy.html"


class AfterLoginRedirectView(RedirectView):
    """Redirect users to the welcome page after first login."""

    def get_redirect_url(self, *args, **kwargs):
        """Get the url to redirect to."""
        next_url = self.request.GET.get("next")
        if self.request.user.is_authenticated and not self.request.user.association:
            messages.add_message(
                self.request, messages.INFO, "Welcome to TOSTI! Please complete your account profile below."
            )
            return reverse("users:account")
        if next_url:
            return next_url
        return reverse("index")


class DocumentationView(TemplateView):
    """Documentation page."""

    template_name = "tosti/documentation.html"


class ExplainerView(TemplateView):
    """Explainer page."""

    template_name = "tosti/explainers.html"
    explainer_tabs = Filter()

    def get(self, request, **kwargs):
        """GET request."""
        tabs = self.explainer_tabs.do_filter([])
        rendered_tabs = []
        for tab in tabs:
            tab_rendered = tab["renderer"](request, tab)
            if tab_rendered is not None:
                rendered_tabs.append({"name": tab["name"], "slug": tab["slug"], "content": tab_rendered})
        return render(request, self.template_name, {"rendered_tabs": rendered_tabs})


def handler403(request, exception):
    """
    Handle a 403 (permission denied) exception.

    :param request: the request
    :param exception: the exception
    :return: a render of the 403 page
    """
    if request.user.is_authenticated:
        return render(request, "tosti/403.html", status=403)
    else:
        return redirect("login")


def handler404(request, exception):
    """
    Handle a 404 (page not found) exception.

    :param request: the request
    :param exception: the exception
    :return: a render of the 404 page
    """
    return render(request, "tosti/404.html", status=404)


def handler500(request, *args, **kwargs):
    """
    Handle a 50x (server fault) exception.

    :param request: the request
    :return: a render of the 500 page
    """
    return render(request, "tosti/500.html", status=500)
