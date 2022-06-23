# Generated by Django 3.2.13 on 2022-06-23 14:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('borrel', '0001_initial'),
        ('venues', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='borrelreservation',
            name='user_created',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='borrel_reservations_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='borrelreservation',
            name='user_submitted',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='borrel_reservations_submitted', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='borrelreservation',
            name='user_updated',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='borrel_reservations_updated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='borrelreservation',
            name='users_access',
            field=models.ManyToManyField(blank=True, related_name='borrel_reservations_access', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='borrelreservation',
            name='venue_reservation',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='borrel_reservations', to='venues.reservation'),
        ),
        migrations.AddField(
            model_name='basicborrelbrevet',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='basic_borrel_brevet', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='reservationitem',
            unique_together={('reservation', 'product')},
        ),
    ]
