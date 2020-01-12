from __future__ import unicode_literals, print_function
from copy import copy
from email.mime.image import MIMEImage
import os
from datetime import datetime
import random

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from guests.models import Party

SAVE_THE_DATE_TEMPLATE = 'guests/email_templates/save_the_date.html'
SAVE_THE_DATE_CONTEXT_MAP = {
    'save-the-date-1': {
        'title': "Save the date 1",
        'header_filename': 'hearts.png',
        'main_image': 'save the date 1.jpg',
        'main_color': '#fff3e8',
        'font_color': '#666666',
    },
    'save-the-date-2': {
        'title': 'Save the date 2',
        'header_filename': 'hearts.png',
        'main_image': 'save the date 2.jpg',
        'main_color': '#330033',
        'font_color': '#ffffff',
    },
    'save-the-date-3': {
        'title': 'Save the date 3',
        'header_filename': 'hearts.png',
        'main_image': 'save the date 3.jpg',
        'main_color': '#ea2e2e',
        'font_color': '#e5ddd9',
    },
    'save-the-date-4': {
        'title': 'Save the date 4',
        'header_filename': 'hearts.png',
        'main_image': 'save the date 4.jpg',
        'main_color': '#ea2e2e',
        'font_color': '#e5ddd9',
    }
}


def send_all_save_the_dates(test_only=False, mark_as_sent=False):
    to_send_to = Party.in_default_order().filter(is_invited=True, save_the_date_sent=None)
    for party in to_send_to:
        send_save_the_date_to_party(party, test_only=test_only)
        if mark_as_sent:
            party.save_the_date_sent = datetime.now()
            party.save()


def send_save_the_date_to_party(party, test_only=False):
    context = get_save_the_date_context(get_template_id_from_party(party))
    recipients = party.guest_emails
    if not recipients:
        print('===== WARNING: no valid email addresses found for {} ====='.format(party))
    else:
        send_save_the_date_email(
            context,
            recipients,
            test_only=test_only
        )


def get_template_id_from_party(party):
    if party.type == 'formal':
        # all formal guests get formal invites
        return random.choice(['lions-head', 'ski-trip'])
    elif party.type == 'dimagi':
        # all non-formal dimagis get dimagi invites
        return 'dimagi'
    elif party.type == 'fun':
        all_options = list(SAVE_THE_DATE_CONTEXT_MAP.keys())
        all_options.remove('dimagi')
        if party.category == 'ro':
            # don't send the canada invitation to ro's crowd
            all_options.remove('canada')
        # otherwise choose randomly from all options for everyone else
        return random.choice(all_options)
    else:
        return None


def get_save_the_date_context(template_id):
    template_id = (template_id or '').lower()
    if template_id not in SAVE_THE_DATE_CONTEXT_MAP:
        template_id = 'lions-head'
    context = copy(SAVE_THE_DATE_CONTEXT_MAP[template_id])
    context['name'] = template_id
    context['page_title'] = 'Ana y Guillem - Save the Date!'
    context['preheader_text'] = (
        "The date that you've eagerly been waiting for is finally here. "
        "Cory and Ro are getting married! Save the date!"
    )
    return context


def send_save_the_date_email(context, recipients, test_only=False):
    context['email_mode'] = True
    context['rsvp_address'] = settings.DEFAULT_WEDDING_REPLY_EMAIL
    context['site_url'] = settings.WEDDING_WEBSITE_URL
    context['couple'] = settings.BRIDE_AND_GROOM
    template_html = render_to_string(SAVE_THE_DATE_TEMPLATE, context=context)
    template_text = "Save the date for {}'s wedding! July 2, 2016. Niagata-on-the-Lake, Ontario, Canada".format(
        settings.BRIDE_AND_GROOM
    )
    subject = 'Save the Date!'
    # https://www.vlent.nl/weblog/2014/01/15/sending-emails-with-embedded-images-in-django/
    msg = EmailMultiAlternatives(subject, template_text, settings.DEFAULT_WEDDING_FROM_EMAIL, recipients,
                                 reply_to=[settings.DEFAULT_WEDDING_REPLY_EMAIL])
    msg.attach_alternative(template_html, "text/html")
    msg.mixed_subtype = 'related'
    for filename in (context['header_filename'], context['main_image']):
        attachment_path = os.path.join(os.path.dirname(__file__), 'static', 'save-the-date', 'images', filename)
        with open(attachment_path, "rb") as image_file:
            msg_img = MIMEImage(image_file.read())
            msg_img.add_header('Content-ID', '<{}>'.format(filename))
            msg.attach(msg_img)

    print('sending {} to {}'.format(context['name'], ', '.join(recipients)))
    if not test_only:
        msg.send()


def clear_all_save_the_dates():
    print('clear')
    for party in Party.objects.exclude(save_the_date_sent=None):
        party.save_the_date_sent = None
        print("resetting {}".format(party))
        party.save()
