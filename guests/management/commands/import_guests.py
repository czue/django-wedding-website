from django.core.management import BaseCommand
from guests import csv_import


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        csv_import.import_guests(kwargs['filename'])

    def add_arguments(self, parser):
        parser.add_argument('filename')
