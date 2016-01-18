import csv
from guests.models import Party, Guest


def import_guests(path):
    with open(path, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        first_row = True
        for row in reader:
            if first_row:
                first_row = False
                continue
            party_name, first_name, last_name, party_type, is_child, category, is_invited, email = row[:8]
            party = Party.objects.get_or_create(name=party_name)[0]
            party.type = party_type
            party.is_invited = _is_true(is_invited)
            party.save()
            if email:
                guest = Guest.objects.get_or_create(party=party, email=email)[0]
                guest.first_name = first_name
                guest.last_name = last_name
            else:
                guest = Guest.objects.get_or_create(party=party, first_name=first_name, last_name=last_name)[0]
            guest.is_child = _is_true(is_child)
            guest.save()


def _is_true(value):
    value = value or ''
    return value.lower() in ('y', 'yes')
