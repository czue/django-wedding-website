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
            party_name, first_name, last_name, email, party_type, is_child = row[:6]
            party = Party.objects.get_or_create(name=party_name)[0]
            if party.type != party_type:
                party.type = party_type
                party.save()
            if email:
                guest = Guest.objects.get_or_create(party=party, email=email)[0]
                guest.first_name = first_name
                guest.last_name = last_name
                guest.save()
            else:
                Guest.objects.get_or_create(party=party, first_name=first_name, last_name=last_name)
