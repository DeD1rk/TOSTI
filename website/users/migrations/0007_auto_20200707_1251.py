# Generated by Django 3.0.5 on 2020-07-07 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('users', '0006_auto_20200707_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupsettings',
            name='group',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.Group'),
        ),
    ]
