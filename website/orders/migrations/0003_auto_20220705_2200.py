# Generated by Django 3.2.13 on 2022-07-05 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['shift', 'prioritize', 'created']},
        ),
        migrations.AddField(
            model_name='order',
            name='prioritize',
            field=models.BooleanField(default=False),
        ),
    ]
