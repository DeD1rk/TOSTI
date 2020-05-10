from datetime import datetime
from decimal import Decimal

from django.conf import settings
import pytz
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from venues.models import Venue

User = get_user_model()


def get_default_start_time_shift():
    """
    Get the default start time of a Shift object.

    :return: the default start time of a shift
    """
    return datetime.now().replace(hour=12, minute=15, second=0, microsecond=0)


def get_default_end_time_shift():
    """
    Get the default end time of a Shift object.

    :return: the default end time of a shift
    """
    return datetime.now().replace(hour=13, minute=15, second=0, microsecond=0)


class Product(models.Model):
    """Products that can be ordered."""

    name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    icon = models.CharField(
        max_length=20,
        unique=True,
        help_text="Font-awesome icon name that is used for quick display of the product type.",
    )
    available = models.BooleanField(default=True, null=False)
    available_at = models.ManyToManyField(Venue)

    current_price = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )

    max_allowed_per_shift = models.PositiveSmallIntegerField(
        verbose_name="Max. allowed orders per shift",
        default=2,
        null=True,
        blank=True,
        help_text="The maximum amount a single user can order this product in a single shift. Note that shifts are "
        "bound to the venue. Empty means no limit.",
    )

    def to_json(self):
        """
        Convert this object to JSON.

        :return: a to JSON convertable dictionary of properties.
        """
        return {
            "name": self.name,
            "icon": self.icon,
            "price": self.current_price,
            "max_per_shift": self.max_allowed_per_shift,
            "available": self.available,
            "id": self.pk,
        }

    def __str__(self):
        """
        Convert a Product object to string.

        :return: the name of the Product object
        """
        return self.name

    def user_can_order_amount(self, user, shift, amount=1):
        """
        Test if a user can order the specified amount of this Product in a specific shift.

        :param user: the user
        :param shift: the shift
        :param amount: the amount that the user wants to order
        :return: True if the already ordered amount of this Product plus the amount specified in the amount parameter
        is lower than the max_allowed_per_shift variable, False otherwise
        """
        user_order_amount_product = Order.objects.filter(
            user=user, shift=shift, product=self
        ).count()
        if (
            self.max_allowed_per_shift is not None
            and user_order_amount_product + amount > self.max_allowed_per_shift
        ):
            return False
        return True

    def user_max_order_amount(self, user, shift):
        """
        Get the maximum amount a user can still order for this product.

        :param user: the user
        :param shift: the shift on which to order the product
        :return: None if the user can order unlimited of the product, the maximum allowed to still order otherwise
        """
        if self.max_allowed_per_shift is not None:
            user_order_amount_product = Order.objects.filter(
                user=user, shift=shift, product=self
            ).count()
            return max(0, self.max_allowed_per_shift - user_order_amount_product)
        else:
            return None

    class Meta:
        """Meta class."""

        ordering = ["-available", "name"]


def active_venue_validator(value):
    """Filter to only allow shifts for active venues."""
    if Venue.objects.get(pk=value).active:
        return True
    else:
        raise ValidationError("This venue is not active.")


class Shift(models.Model):
    """Shifts in which orders can be placed."""

    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M"

    venue = models.ForeignKey(
        Venue,
        blank=False,
        null=False,
        on_delete=models.PROTECT,
        validators=[active_venue_validator],
    )

    start_date = models.DateTimeField(
        blank=False, null=False, default=get_default_start_time_shift,
    )
    end_date = models.DateTimeField(
        blank=False, null=False, default=get_default_end_time_shift,
    )

    can_order = models.BooleanField(
        verbose_name="Orders allowed",
        default=False,
        blank=False,
        null=False,
        help_text="If checked, people can order within the given time frame. If not checked, ordering will not be "
        "possible, even in the given time frame.",
    )

    max_orders_per_user = models.PositiveSmallIntegerField(
        verbose_name="Max. number of orders per user",
        default=2,
        null=True,
        blank=True,
        help_text="The maximum amount of products a single user can order in this shift. Empty means no limit.",
    )

    max_orders_total = models.PositiveSmallIntegerField(
        verbose_name="Max. total number of orders",
        default=50,
        null=True,
        blank=True,
        help_text="The maximum amount of products that can be ordered during this shift in total. Empty means no "
        "limit.",
    )

    assignees = models.ManyToManyField(User)

    @property
    def orders(self):
        """
        Get the orders of this shift.

        :return: a Queryset with the orders of this shift.
        """
        return Order.objects.filter(shift=self).order_by("user", "created")

    @property
    def number_of_orders(self):
        """
        Get the total number of orders in this shift.

        :return: the total number of orders in this shift
        """
        return Order.objects.filter(shift=self).count()

    @property
    def max_orders_total_string(self):
        """
        Get the maximum amount of orders in string format.

        :return: the maximum amount of orders in string format
        """
        if self.max_orders_total:
            return self.max_orders_total
        return "∞"

    @property
    def capacity(self):
        """
        Get the current capacity of a shift as a string.

        :return: the current capacity of a shift in string format
        """
        return f"{self.number_of_orders} / {self.max_orders_total_string}"

    @property
    def is_active(self):
        """
        Check if a shift is currently active.

        :return: True if the current time is between the start_date and end_date of this shift
        """
        timezone = pytz.timezone(settings.TIME_ZONE)
        current_time = timezone.localize(datetime.now())
        return self.start_date < current_time < self.end_date

    @property
    def date(self):
        """
        Get the date of this object in string format.

        :return: the date of this object in string format
        """
        if self.start_date.date() == self.end_date.date():
            return f"{self.start_date.strftime(self.DATE_FORMAT)}"
        return f"{self.start_date.strftime(self.DATE_FORMAT)} - {self.end_date.strftime(self.DATE_FORMAT)}"

    @property
    def start_time(self):
        """
        Get the start time of this object in string format.

        :return: the start time of this object in string format
        """
        return f"{self.start_date.strftime(self.TIME_FORMAT)}"

    @property
    def end_time(self):
        """
        Get the end time of this object in string format.

        :return: the end time of this object in string format
        """
        return f"{self.end_date.strftime(self.TIME_FORMAT)}"

    @property
    def get_assignees(self):
        """
        Get assignees of this shift.

        :return: a QuerySet with User objects of assignees of this shift
        """
        return self.assignees.all()

    def __str__(self):
        """
        Convert this object to string.

        :return: this object in string format
        """
        return f"{self.venue} {self.date}"

    def save(self, *args, **kwargs):
        """
        Save an object of the Shift type.

        :param args: arguments
        :param kwargs: keyword arguments
        :return: an instance of the Shift object if the saving succeeded, raises a ValueError on error
        """
        if self.end_date <= self.start_date:
            raise ValueError(f"End date cannot be before start date.")

        overlapping_start = (
            Shift.objects.filter(
                start_date__gte=self.start_date,
                start_date__lte=self.end_date,
                venue=self.venue,
            )
            .exclude(pk=self.pk)
            .count()
        )
        overlapping_end = (
            Shift.objects.filter(
                end_date__gte=self.start_date,
                end_date__lte=self.end_date,
                venue=self.venue,
            )
            .exclude(pk=self.pk)
            .count()
        )
        if overlapping_start > 0 or overlapping_end > 0:
            raise ValueError("Overlapping shifts for the same venue are not allowed.")

        super(Shift, self).save(*args, **kwargs)

    def user_can_order_amount(self, user, amount=1):
        """
        Test if a user can order a specific amount of products.

        :param user: the user
        :param amount: the amount that the user wants to order
        :return: True if the user is allowed to order amount of products, False otherwise
        """
        user_order_amount = Order.objects.filter(user=user, shift=self).count()
        if (
            self.max_orders_per_user is not None
            and user_order_amount + amount > self.max_orders_per_user
        ):
            return False

        return True

    def user_max_order_amount(self, user):
        """
        Get the maximum a user can still order in this shift.

        :param user: the user
        :return: the maximum of orders a user can still place in this shift, None if there is no maximum specified
        """
        if self.max_orders_per_user is not None:
            user_order_amount = Order.objects.filter(user=user, shift=self).count()
            return max(0, self.max_orders_per_user - user_order_amount)
        else:
            return None

    def update_can_order(self):
        """Update the can_order field from a shift when an order is placed."""
        if self.order_set.count() >= self.max_orders_total:
            self.can_order = False
            self.save()

    class Meta:
        """Meta class."""

        ordering = ["start_date", "end_date"]


def available_product_filter(value):
    """Filter to only allow ordering available products."""
    if Product.objects.get(pk=value).available:
        return True
    else:
        raise ValidationError("This product is not available.")


class Order(models.Model):
    """
    A user that ordered a product.

    Orders only contain a single product. If a user orders multiple products
    (or multiple amounts of products) he or she must place multiple orders.
    Verifying the amount of allowed orders is done via Shifts.
    """

    created = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.PROTECT)
    shift = models.ForeignKey(Shift, blank=False, null=False, on_delete=models.PROTECT,)
    product = models.ForeignKey(
        Product,
        blank=False,
        null=False,
        on_delete=models.PROTECT,
        validators=[available_product_filter],
    )

    order_price = models.DecimalField(max_digits=6, decimal_places=2)

    ready = models.BooleanField(default=False, null=False)
    ready_at = models.DateTimeField(null=True, blank=True)

    paid = models.BooleanField(default=False, null=False)
    paid_at = models.DateTimeField(null=True, blank=True)

    delivered = models.BooleanField(default=False, null=False)
    delivered_at = models.DateTimeField(null=True, blank=True)

    def to_json(self):
        """
        Convert this object to JSON.

        :return: a to JSON convertable dictionary of properties.
        """
        return {
            "id": self.pk,
            "user": self.user.username,
            "product": self.product.to_json(),
            "price": self.order_price,
            "paid": self.paid,
            "delivered": self.delivered,
        }

    def __str__(self):
        """
        Convert this object to string.

        :return: string format of this object
        """
        return f"{self.product} for {self.user} ({self.shift})"

    def clean(self):
        """Check whether this order is valid and can be saved."""
        super().clean()
        errors = {}

        if not self.created and not self.shift.can_order:
            errors.update({"shift": "You can't order for this shift"})

        if self.created and not (
            self.shift.start_date < self.created < self.shift.end_date
        ):
            errors.update({"shift": "You can't order for this shift"})

        if (
            self.shift.max_orders_per_user is not None
            and Order.objects.filter(shift=self.shift, user=self.pk)
            .exclude(pk=self.pk)
            .count()
            >= self.shift.max_orders_per_user
        ):
            errors.update(
                {
                    "shift": f"You are not allowed to order more than {self.shift.max_orders_per_user} "
                    f"products in this shift."
                }
            )
        if (
            self.product.max_allowed_per_shift is not None
            and Order.objects.filter(product=self.product, user=self.pk)
            .exclude(pk=self.pk)
            .count()
            >= self.product.max_allowed_per_shift
        ):
            errors.update(
                {
                    "product": f"You are not allowed to order more than {self.product.max_allowed_per_shift} "
                    f"products of this kind in this shift."
                }
            )

        if self.delivered and not self.ready:
            errors.update({"delivered": f"Product can't be delivered but not ready"})

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """
        Save an object of the Order type.

        :param args: arguments
        :param kwargs: keyword arguments
        :return: an instance of the Order object if the saving succeeded, raises a ValueError on error
        """
        if not self.order_price:
            self.order_price = self.product.current_price

        super(Order, self).save(*args, **kwargs)

    @property
    def get_venue(self):
        """
        Get the venue of this Order.

        :return: the venue associated to this Order
        """
        return self.shift.venue

    class Meta:
        """Meta class."""

        ordering = ["created"]
