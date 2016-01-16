from django.core.management import BaseCommand
from guests import csv_import


class Command(BaseCommand):
    args = 'filename'

    def handle(self, filename, *args, **kwargs):
        csv_import.import_guests(filename)
