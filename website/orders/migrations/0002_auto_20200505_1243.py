# Generated by Django 3.0.5 on 2020-05-05 10:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="shift",
            name="end_date",
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 5, 13, 15)),
        ),
        migrations.AlterField(
            model_name="shift",
            name="start_date",
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 5, 12, 15)),
        ),
    ]
