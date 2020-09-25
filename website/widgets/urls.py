from django.urls import path, register_converter

from widgets import views
from venues.converters import VenueConverter


register_converter(VenueConverter, "venue")

urlpatterns = [
    path("<venue:venue>", views.DashboardView.as_view(), name="dashboard"),
]
