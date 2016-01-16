import os
from django.test import TestCase
from guests.csv_import import import_guests
from guests.models import Party, Guest


class GuestImporterTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super(GuestImporterTest, cls).setUpClass()
        cls.path = os.path.join(os.path.dirname(__file__), 'data', 'guests-test.csv')

    def test_import(self):
        import_guests(self.path)
        self.assertEqual(2, Party.objects.count())
        self.assertEqual(4, Guest.objects.count())
        the_starks = Guest.objects.filter(party__name='The Starks')
        self.assertEqual(3, the_starks.count())

    def test_import_idempotent(self):
        for i in range(3):
            import_guests(self.path)
            self.assertEqual(2, Party.objects.count())
            self.assertEqual(4, Guest.objects.count())
            the_starks = Guest.objects.filter(party__name='The Starks')
            self.assertEqual(3, the_starks.count())
