import logging

import spotipy
from django.http import JsonResponse, Http404
from django.shortcuts import render, redirect
from django.template.loader import get_template, render_to_string
from django.views.generic import TemplateView
from .forms import SpotifyTokenForm
from django.urls import reverse
from .models import SpotifySettings, SpotifyArtist, SpotifyQueueItem
from .services import create_track_database_information
from .templatetags.queue import render_queue_list

COOKIE_CLIENT_ID = "client_id"


class NowPlayingView(TemplateView):
    """Now playing view."""

    template_name = "marietje/now_playing.html"

    def get(self, request, **kwargs):
        """
        GET request for NowPlayingView.

        :param request: the request
        :param kwargs: keyword arguments
        :return: a render of the now playing page
        """
        venue = kwargs.get("venue")
        if not venue.has_player or not venue.spotify_player.configured:
            return render(
                request, self.template_name, {"disabled": True, "venue": venue}
            )

        return render(
            request,
            self.template_name,
            {
                "disabled": False,
                "player": venue.spotify_player.currently_playing,
                "auth": venue.spotify_player,
            },
        )


class SpofityAuthorizeView(TemplateView):
    """Authorize a Spotify account."""

    template_name = "marietje/authorize.html"

    def get(self, request, **kwargs):
        """
        GET request for SpotifyAuthorizeView.

        :param request: the request
        :param kwargs: keyword arguments
        :return: a render of the authorize page
        """
        form = SpotifyTokenForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, **kwargs):
        """
        POST request for SpotifyAuthorizeView.

        :param request: the request
        :param kwargs: keyword arguments
        :return: either a render of the authorize page on error or a redirect to the authorization url otherwise
        """
        form = SpotifyTokenForm(request.POST)
        if form.is_valid():
            spotify_auth_code, _ = SpotifySettings.objects.get_or_create(
                client_id=form.cleaned_data.get("client_id")
            )
            spotify_auth_code.client_secret = form.cleaned_data.get("client_secret")
            spotify_auth_code.redirect_uri = request.build_absolute_uri(
                reverse("marietje:add_token")
            )
            spotify_auth_code.save()
            spotify_oauth = redirect(spotify_auth_code.auth.get_authorize_url())
            spotify_oauth.set_cookie(COOKIE_CLIENT_ID, spotify_auth_code.client_id)
            return spotify_oauth
        return render(request, self.template_name, {"form": form})


class SpotifyTokenView(TemplateView):
    """Get a Spotify account token."""

    template_name = "marietje/token.html"

    def get(self, request, **kwargs):
        """
        GET request for SpotifyAuthorizeView.

        :param request: the request
        :param kwargs: keyword arguments
        :return: a render of the authorize page
        """
        code = request.GET.get("code", None)
        if code is not None:
            client_id = request.COOKIES.get(COOKIE_CLIENT_ID, None)
            try:
                spotify_auth_code = SpotifySettings.objects.get(client_id=client_id)
            except SpotifySettings.DoesNotExist:
                return render(
                    request, self.template_name, {"error": "Client ID was not found."}
                )
            # Generate the first access token and store in cache
            access_token = spotify_auth_code.auth.get_access_token(code=code)
            if access_token is not None:
                response = redirect(
                    "marietje:authorization_succeeded", auth=spotify_auth_code
                )
            else:
                response = render(
                    request,
                    self.template_name,
                    {"Error": "Access token retrieval failed, please try again."},
                )
            response.delete_cookie(COOKIE_CLIENT_ID)
            return response
        else:
            return render(
                request,
                self.template_name,
                {
                    "error": "No Spotify code found, make sure you are reaching this"
                    "page via a Spotify redirect."
                },
            )


class SpotifyAuthorizeSucceededView(TemplateView):
    """Authorize succeeded view."""

    template_name = "marietje/authorize_succeeded.html"

    def get(self, request, **kwargs):
        """
        GET request for Spotify Authorize Succeeded view.

        :param request: the request
        :param kwargs: keyword arguments
        :return: a render of the authorize succeeded page
        """
        auth = kwargs.get("auth")
        return render(
            request,
            self.template_name,
            {"username": auth.get_display_name, "auth": auth},
        )


class PlayerRefreshView(TemplateView):
    """Refresh the player."""

    def post(self, request, **kwargs):
        """
        POST request for refreshing the player.

        :param request: the request
        :param kwargs: keyword arguments
        :return: The player in the following JSON format:
        {
            data: [player]
        }
        """
        spotify = kwargs.get("auth")
        player = get_template("marietje/player.html").render(
            {"player": spotify.currently_playing, "auth": spotify}
        )
        return JsonResponse({"data": player})


class QueueRefreshView(TemplateView):
    """Refresh the queue."""

    def post(self, request, **kwargs):
        """
        POST request for refreshing the queue.

        :param request: the request
        :param kwargs: keyword arguments
        :return: The player in the following JSON format:
        {
            data: [queue]
        }
        """
        spotify = kwargs.get("auth")
        queue = get_template("marietje/queue.html").render(
            render_queue_list(spotify, refresh=True)
        )
        return JsonResponse({"data": queue})


def search_view(request, **kwargs):

    if request.method == "POST":
        query = request.POST.get("query", None)
        request_id = request.POST.get("id", "")
        try:
            maximum = int(request.POST.get("maximum", 5))
        except ValueError:
            maximum = 5

        if query is not None:
            spotify = kwargs.get("auth")
            result = spotify.spotify.search(query, limit=maximum, type="track")
            result = sorted(result["tracks"]["items"], key=lambda x: -x["popularity"])
            trimmed_result = [
                {
                    "name": x["name"],
                    "artists": [y["name"] for y in x["artists"]],
                    "id": x["id"],
                }
                for x in result
            ]
            rendered_results = render_to_string(
                "marietje/search.html", {"refresh": True, "tracks": trimmed_result}
            )
            return JsonResponse(
                {"query": query, "id": request_id, "result": rendered_results}
            )
        else:
            return JsonResponse({"query": "", "id": request_id, "result": ""})
    else:
        return Http404("This view can only be called with a POST request.")


def add_view(request, **kwargs):

    if request.method == "POST":
        track_id = request.POST.get("id", None)
        if track_id is not None:
            spotify = kwargs.get("auth")
            try:
                track_info = spotify.spotify.track(track_id)
                track = create_track_database_information(track_info)
                SpotifyQueueItem.objects.create(
                    track=track,
                    spotify_settings_object=spotify,
                    requested_by=request.user,
                )
                spotify.spotify.add_to_queue(
                    track_id, device_id=spotify.playback_device_id
                )
            except spotipy.exceptions.SpotifyException as e:
                logging.error(e)
                return JsonResponse(
                    {"error": True, "msg": "The track could not be added to the queue"}
                )
            return JsonResponse({"error": False, "msg": "Track added to queue"})
        else:
            return JsonResponse({"error": True, "msg": "No track ID specified"})
    else:
        return Http404("This view can only be called with a POST request.")
