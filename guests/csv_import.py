import csv
import uuid
from io import StringIO

from guests.models import Party, Guest


def import_guests(path):
    with open(path, 'r', encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            print(row)

            party = Party.objects.get_or_create(name=row['Party Name'])[0]
            party.is_invited = True
            party.lang = row['Language']
            if not party.invitation_id:
                party.invitation_id = uuid.uuid4().hex
            party.save()

            email = row.get('Email')
            first_name = row['First Name']
            last_name = row['Last Name']

            if email:
                guest, created = Guest.objects.get_or_create(party=party, email=email)
                guest.first_name = first_name
                guest.last_name = last_name
            else:
                guest = Guest.objects.get_or_create(party=party, first_name=first_name, last_name=last_name)[0]
            # guest.is_child = _is_true(is_child)
            guest.save()


def export_guests():
    headers = [
        'party_name', 'first_name', 'last_name', 'party_type',
        'is_child', 'category', 'is_invited', 'is_attending',
        'rehearsal_dinner', 'meal', 'email', 'comments'
    ]
    file = StringIO()
    writer = csv.writer(file)
    writer.writerow(headers)
    for party in Party.in_default_order():
        for guest in party.guest_set.all():
            if guest.is_attending:
                writer.writerow([
                    party.name,
                    guest.first_name,
                    guest.last_name,
                    party.type,
                    guest.is_child,
                    party.category,
                    party.is_invited,
                    guest.is_attending,
                    party.rehearsal_dinner,
                    guest.meal,
                    guest.email,
                    party.comments,
                ])
    return file


def _is_true(value):
    value = value or ''
    return value.lower() in ('y', 'yes')
