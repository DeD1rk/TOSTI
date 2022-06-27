# Generated by Django 3.2.13 on 2022-06-24 11:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('associations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('active', models.BooleanField(default=True)),
                ('color_in_calendar', models.CharField(blank=True, help_text='Color of reservations shown in calendar.', max_length=50, null=True)),
                ('can_be_reserved', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['-active', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('comment', models.TextField(blank=True, null=True)),
                ('accepted', models.BooleanField(blank=True, default=None, null=True)),
                ('association', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reservations', to='associations.association')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reservations', to=settings.AUTH_USER_MODEL)),
                ('venue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='venues.venue')),
            ],
        ),
    ]
