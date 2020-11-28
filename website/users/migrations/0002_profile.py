# Generated by Django 3.0.8 on 2020-11-26 09:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def create_profiles(apps, schema_editor):
    Profile = apps.get_model("users", "Profile")
    User = apps.get_model("users", "User")
    users = User.objects.all()
    for user in users:
        Profile.objects.get_or_create(user=user)


class Migration(migrations.Migration):

    dependencies = [
        ('associations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('association', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='associations.Association')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RunPython(create_profiles),
    ]
