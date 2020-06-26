# Generated by Django 3.0.5 on 2020-06-25 10:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("venues", "0002_remove_venue_image"),
    ]

    operations = [
        migrations.CreateModel(
            name="SpotifyAccount",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "display_name",
                    models.CharField(blank=True, max_length=256, null=True),
                ),
                (
                    "playback_device_id",
                    models.CharField(blank=True, max_length=256, null=True),
                ),
                (
                    "playback_device_name",
                    models.CharField(blank=True, max_length=256, null=True),
                ),
                ("client_id", models.CharField(max_length=256, unique=True)),
                ("client_secret", models.CharField(max_length=256)),
                ("redirect_uri", models.CharField(max_length=512)),
                (
                    "venue",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="venues.Venue",
                    ),
                ),
            ],
            options={
                "verbose_name": "Spotify settings",
                "verbose_name_plural": "Spotify settings",
            },
        ),
        migrations.CreateModel(
            name="SpotifyArtist",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("artist_name", models.CharField(max_length=2048, unique=True)),
                ("artist_id", models.CharField(max_length=2048)),
            ],
        ),
        migrations.CreateModel(
            name="SpotifyTrack",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("track_id", models.CharField(max_length=256, unique=True)),
                ("track_name", models.CharField(max_length=1024)),
                ("track_artists", models.ManyToManyField(to="marietje.SpotifyArtist")),
            ],
        ),
        migrations.CreateModel(
            name="SpotifyQueueItem",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("added", models.DateTimeField(auto_now_add=True)),
                (
                    "requested_by",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "spotify_settings_object",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="marietje.SpotifyAccount",
                    ),
                ),
                (
                    "track",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="marietje.SpotifyTrack",
                    ),
                ),
            ],
            options={"ordering": ["-added"],},
        ),
    ]
