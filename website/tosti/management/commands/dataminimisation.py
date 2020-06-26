import logging

from django.core.management import BaseCommand

import marietje.services
import orders.services
import users.services


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            dest="dry-run",
            default=False,
            help="Dry run instead of saving data",
        )

    def handle(self, *args, **options):
        processed_orders = orders.services.execute_data_minimisation(options["dry-run"])
        for p in processed_orders:
            logging.info("Removed order data for {}".format(p))
        processed_marietje = marietje.services.execute_data_minimisation(options["dry-run"])
        for p in processed_marietje:
            logging.info("Removed marietje data for {}".format(p))
        processed_users = users.services.execute_data_minimisation(options["dry-run"])
        for p in processed_users:
            logging.info("Removed user account for {}".format(p))
0
