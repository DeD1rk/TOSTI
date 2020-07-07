# Generated by Django 3.0.5 on 2020-07-06 12:00

import django.contrib.auth.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0011_update_proxy_permissions"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Group",
            fields=[],
            options={"proxy": True, "indexes": [], "constraints": [],},
            bases=("auth.group",),
            managers=[("objects", django.contrib.auth.models.GroupManager()),],
        ),
        migrations.DeleteModel(name="User",),
        migrations.CreateModel(
            name="User",
            fields=[],
            options={"proxy": True, "indexes": [], "constraints": [],},
            bases=("auth.user",),
        ),
    ]
