from django.urls import path, register_converter

from orders import views
from .converters import ShiftConverter, VenueConverter, OrderConverter

register_converter(ShiftConverter, "shift")
register_converter(VenueConverter, "venue")
register_converter(OrderConverter, "order")

urlpatterns = [
    path("explainer/", views.ExplainerView.as_view(), name="explainer"),
    path("explainer-admin/", views.AdminExplainerView.as_view(), name="explainer_admin"),
    path("<shift:shift>/order-items/", views.PlaceOrderView.as_view(), name="order"),
    path("venue/<venue:venue>/create/", views.CreateShiftView.as_view(), name="shift_create"),
    path("<shift:shift>/admin/", views.ShiftAdminView.as_view(), name="shift_admin"),
    path("<shift:shift>/admin/scanner", views.ShiftScannerView.as_view(), name="shift_admin_scanner"),
    path("<shift:shift>/admin/search", views.ProductSearchView.as_view(), name="shift_admin_search"),
    path("order/<order:order>/update/", views.OrderUpdateView.as_view(), name="order_update"),
    path("order/<order:order>/remove", views.OrderRemoveView.as_view(), name="order_remove"),
    path("<shift:shift>/products/", views.ProductListView.as_view(), name="product_list"),
    path("<shift:shift>/products/add", views.ProductAddView.as_view(), name="add_product"),
    path("<shift:shift>/overview/", views.ShiftOverviewView.as_view(), name="shift_overview"),
    path("<shift:shift>/control/toggle/", views.ToggleShiftActivationView.as_view(), name="shift_toggle"),
    path("<shift:shift>/control/add-time/", views.AddShiftTimeView.as_view(), name="shift_add_time"),
    path("<shift:shift>/control/add-capacity/", views.AddShiftCapacityView.as_view(), name="shift_add_capacity"),
    path("<shift:shift>/join/", views.JoinShiftView.as_view(), name="shift_join"),
    path("<shift:shift>/refresh/header/", views.RefreshShiftHeaderView.as_view(), name="shift_refresh_header"),
    path("<shift:shift>/refresh/footer/", views.RefreshAdminFooterView.as_view(), name="shift_refresh_admin_footer"),
    path(
        "<shift:shift>/refresh/overview/",
        views.RefreshShiftSummaryView.as_view(),
        name="shift_refresh_product_overview",
    ),
    path("<shift:shift>/refresh/orders/", views.RefreshShiftOrderView.as_view(), name="shift_refresh_orders"),
]
