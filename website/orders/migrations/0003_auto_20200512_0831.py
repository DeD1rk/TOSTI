# Generated by Django 3.0.5 on 2020-05-12 06:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0002_auto_20200508_1844"),
    ]

    operations = [
        migrations.RemoveField(model_name="order", name="delivered",),
        migrations.RemoveField(model_name="order", name="delivered_at",),
    ]
