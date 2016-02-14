import uuid
from datetime import datetime
from django.test import TestCase
from django.utils import timezone
from guests.models import Party, track_invitation_opened


class InvitationTrackerTest(TestCase):

    def setUp(self):
        self.invitation_id = uuid.uuid4().hex
        self.party = Party.objects.create(
            name='The Starks',
            type='formal',
            invitation_id=self.invitation_id
        )

    def get_latest_party(self):
        return Party.objects.get(pk=self.party.pk)

    def test_not_found(self):
        track_invitation_opened(uuid.uuid4().hex)
        self.assertEqual(None, self.get_latest_party().invitation_opened)

    def test_update_status(self):
        before = datetime.now(tz=timezone.UTC())
        track_invitation_opened(self.invitation_id)
        after = datetime.now(tz=timezone.UTC())
        self.assertTrue(before <= self.get_latest_party().invitation_opened <= after)
