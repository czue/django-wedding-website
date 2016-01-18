from email.mime.image import MIMEImage
import os
from datetime import datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from guests.models import Party


SAVE_THE_DATE_TEMPLATE = 'guests/email_templates/save_the_date.html'


def send_all_save_the_dates(test_only=False, mark_as_sent=False):
    to_send_to = Party.objects.filter(is_invited=True, save_the_date_sent=None)
    for party in to_send_to:
        send_save_the_date_to_party(party, test_only=test_only)
        if mark_as_sent:
            party.save_the_date_sent = datetime.now()
            party.save()


def send_save_the_date_to_party(party, test_only=False):
    context = get_save_the_date_context(get_template_id_from_party(party))
    send_save_the_date_email(
        context,
        filter(None, party.guest_set.values_list('email', flat=True)),
        test_only=test_only
    )


def get_template_id_from_party(party):
    if party.type == 'formal':
        return 'classy'
    elif party.type == 'fun':
        return 'canada'
    else:
        return None


def get_save_the_date_context(template_id):
    context_map = {
        'classy': {
            'header_filename': 'hearts.png',
            'main_image': 'selfie.jpg',
            'main_color': '#fff3e8',
            'font_color': '#666666',
        },
        'canada': {
            'header_filename': 'maple-leaf.png',
            'main_image': 'canada-cartoon.jpg',
            'main_color': '#ea2e2e',
            'font_color': '#e5ddd9',
        }
    }
    template_id = (template_id or '').lower()
    if template_id not in context_map:
        template_id = 'classy'
    return context_map[template_id]


def send_save_the_date_email(context, recipients, test_only=False):
    context['email_mode'] = True
    template_html = render_to_string(SAVE_THE_DATE_TEMPLATE, context=context)
    template_text = 'sorry, you need to view this in html mode'
    subject = 'save the date!'
    # https://www.vlent.nl/weblog/2014/01/15/sending-emails-with-embedded-images-in-django/
    msg = EmailMultiAlternatives(subject, template_text, 'hello@coryandro.com', recipients)
    msg.attach_alternative(template_html, "text/html")
    msg.mixed_subtype = 'related'
    for filename in (context['header_filename'], context['main_image']):
        attachment_path = os.path.join(os.path.dirname(__file__), 'static', 'save-the-date', 'images', filename)
        with open(attachment_path, "rb") as image_file:
            msg_img = MIMEImage(image_file.read())
            msg_img.add_header('Content-ID', '<{}>'.format(filename))
            msg.attach(msg_img)

    print u'sending {} to {}'.format(context['main_image'], ', '.join(recipients))
    if not test_only:
        msg.send()


def clear_all_save_the_dates():
    for party in Party.objects.exclude(save_the_date_sent=None):
        party.save_the_date_sent = None
        party.save()
