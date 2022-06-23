# Generated by Django 3.2.13 on 2022-06-23 14:07

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import orders.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('associations', '0001_initial'),
        ('venues', '0001_initial'),
        ('orders', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderVenue',
            fields=[
                ('venue', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='venues.venue')),
            ],
            options={
                'ordering': ['venue__name'],
                'permissions': [('can_order_in_venue', 'Can order products during shifts in this venue'), ('can_manage_shift_in_venue', 'Can manage shifts in this venue')],
            },
        ),
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(default=orders.models.get_default_start_time_shift)),
                ('end', models.DateTimeField(default=orders.models.get_default_end_time_shift)),
                ('can_order', models.BooleanField(default=False, help_text='If checked, people can order within the given time frame. If not checked, ordering will not be possible, even in the given time frame.', verbose_name='Orders allowed')),
                ('finalized', models.BooleanField(default=False, help_text='If checked, shift is finalized and no alterations on the shift can be made anymore.', verbose_name='Shift finalized')),
                ('max_orders_per_user', models.PositiveSmallIntegerField(blank=True, default=2, help_text='The maximum amount of products a single user can order in this shift. Empty means no limit.', null=True, verbose_name='Max. number of orders per user')),
                ('max_orders_total', models.PositiveSmallIntegerField(blank=True, default=50, help_text='The maximum amount of products that can be ordered during this shift in total. Empty means no limit.', null=True, verbose_name='Max. total number of orders')),
                ('assignees', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('venue', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='shifts', to='orders.ordervenue', validators=[orders.models.active_venue_validator])),
            ],
            options={
                'ordering': ['-start', '-end'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('icon', models.CharField(blank=True, default='', help_text='Font-awesome icon name that is used for quick display of the product type.', max_length=20)),
                ('available', models.BooleanField(default=True)),
                ('current_price', models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
                ('orderable', models.BooleanField(default=True, help_text='Whether or not this product should appear on the order page.')),
                ('ignore_shift_restrictions', models.BooleanField(default=False, help_text='Whether or not this product should ignore the maximum orders per shift restriction.')),
                ('max_allowed_per_shift', models.PositiveSmallIntegerField(blank=True, default=2, help_text='The maximum amount a single user can order this product in a single shift. Note that shifts are bound to the venue. Empty means no limit.', null=True, verbose_name='Max. allowed orders per shift')),
                ('barcode', models.CharField(blank=True, default=None, help_text='Either an EAN-8 or EAN-13 barcode.', max_length=13, null=True, unique=True, validators=[orders.models.validate_barcode])),
                ('available_at', models.ManyToManyField(to='orders.OrderVenue')),
            ],
            options={
                'ordering': ['-available', 'name'],
            },
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='orders.product', validators=[orders.models.available_product_filter]),
        ),
        migrations.AddField(
            model_name='order',
            name='shift',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='orders.shift'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='orders', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='order',
            name='user_association',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='associations.association'),
        ),
    ]
