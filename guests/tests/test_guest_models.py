from django.test import TestCase
from guests.models import Party, Guest


class PartyTest(TestCase):

    def setUp(self):
        self.party = Party.objects.create(
            name='The Starks',
            type='formal',
        )
        self.guest1 = Guest.objects.create(
            party=self.party,
            first_name='Ned',
            last_name='Stark',
        )
        self.guest2 = Guest.objects.create(
            party=self.party,
            first_name='Catelyn',
            last_name='Stark',
        )

    def tearDown(self):
        Party.objects.all().delete()

    def test_any_guests_attending_default(self):
        self.assertFalse(self.party.any_guests_attending)

    def test_any_guests_attending_false(self):
        self.guest1.is_attending = False
        self.guest1.save()
        self.guest2.is_attending = False
        self.guest2.save()
        self.assertFalse(self.party.any_guests_attending)

    def test_any_guests_attending_true(self):
        self.guest1.is_attending = False
        self.guest1.save()
        self.guest2.is_attending = True
        self.guest2.save()
        self.assertTrue(self.party.any_guests_attending)
