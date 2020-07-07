from django.urls import path, register_converter

from marietje import views
from .converters import SpotifyAccountConverter
from venues.converters import VenueConverter


register_converter(VenueConverter, "venue")
register_converter(SpotifyAccountConverter, "player")

urlpatterns = [
    path("index", views.IndexView.as_view(), name="index"),
    path("player/<venue:venue>", views.NowPlayingView.as_view(), name="now_playing"),
    path("player/<player:player>/refresh", views.PlayerRefreshView.as_view(), name="player_refresh",),
    path("player/<player:player>/queue/refresh", views.QueueRefreshView.as_view(), name="queue_refresh",),
    path("player/<player:player>/search", views.SearchView.as_view(), name="player_search"),
    path("player/<player:player>/add", views.AddView.as_view(), name="player_add"),
    path("player/<player:player>/play", views.PlayView.as_view(), name="player_play"),
    path("player/<player:player>/pause", views.PauseView.as_view(), name="player_pause"),
    path("player/<player:player>/next", views.NextView.as_view(), name="player_next"),
    path("player/<player:player>/previous", views.PreviousView.as_view(), name="player_previous"),
]
