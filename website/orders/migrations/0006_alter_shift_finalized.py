# Generated by Django 3.2.9 on 2021-12-10 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_shift_finalized'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shift',
            name='finalized',
            field=models.BooleanField(default=False, help_text='If checked, shift is finalized and no alterations on the shift can be made anymore.', verbose_name='Shift finalized'),
        ),
    ]
