import csv
import io
import uuid
from guests.models import Party, Guest
#try:
#    from StringIO import StringIO
#except ImportError:
from io import StringIO


def import_guests(path):
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        first_row = True
        for row in reader:
            if first_row:
                first_row = False
                continue
            party_name, first_name, last_name, email, address, is_child, family, is_invited = row[:8]
            if not party_name:
                print ('skipping row {}'.format(row))
                continue
            party = Party.objects.get_or_create(name=party_name)[0]
            if family == 'jacob' or family == 'jake' or family == 'Jacob' or family == 'Jake':
                party.family = 'jacob'
            else:
                party.family = 'kim'
            if party.address == '':
                party.address = address
            if party.rsvp_code == '':
                party.rsvp_code = (last_name + first_name).lower().replace(" ", "")
            party.family == family
            party.is_invited = _is_true(is_invited)
            if not party.invitation_id:
                party.invitation_id = uuid.uuid4().hex
            party.save()
            guest = Guest.objects.get_or_create(party=party, first_name=first_name, last_name=last_name, email=email)[0]
            guest.is_child = _is_true(is_child)
            guest.save()


def export_guests():
    headers = [
        'party_name', 'rsvp_code','first_name', 'last_name', 'family',
        'is_child', 'is_invited', 'is_attending',
        'tea_ceremony', 'meal', 'email', 'comments'
    ]
    file = io.StringIO()
    writer = csv.writer(file)
    writer.writerow(headers)
    for party in Party.in_default_order():
        for guest in party.guest_set.all():
            writer.writerow([
                party.name,
                party.rsvp_code,
                guest.first_name,
                guest.last_name,
                party.family,
                guest.is_child,
                party.is_invited,
                guest.is_attending,
                guest.tea_ceremony,
                guest.meal,
                guest.email,
                party.comments,
                ])
    return file


def _is_true(value):
    value = value or ''
    return value.lower() in ('y', 'yes', 't', 'true', '1')
