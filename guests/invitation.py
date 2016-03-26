from email.mime.image import MIMEImage
import os
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.http import Http404
from django.template.loader import render_to_string
from guests.models import Party, MEALS

INVITATION_TEMPLATE = 'guests/email_templates/invitation.html'


def guess_party_by_invite_id_or_404(invite_id):
    try:
        return Party.objects.get(invitation_id=invite_id)
    except Party.DoesNotExist:
        if settings.DEBUG:
            # in debug mode allow access by ID
            return Party.objects.get(id=int(invite_id))
        else:
            raise Http404()


def get_invitation_context(party):
    return {
        'title': "Lion's Head",
        'main_image': 'bride-groom.png',
        'main_color': '#fff3e8',
        'font_color': '#666666',
        'page_title': "Cory and Rowena - You're Invited!",
        'preheader_text': "Lucky you! You made the cut!",  # todo: make better
        'invitation_id': party.invitation_id,
        'party': party,
        'meals': MEALS,
    }


def send_invitation_email(context, recipients, test_only=False):
    context['email_mode'] = True
    template_html = render_to_string(INVITATION_TEMPLATE, context=context)
    template_text = "You're invited to Cory and Rowena's wedding. To view this invitation, visit {} in any browser.".format(
        reverse('invitation', args=[context['invitation_id']])
    )
    subject = "You're invited"
    # https://www.vlent.nl/weblog/2014/01/15/sending-emails-with-embedded-images-in-django/
    msg = EmailMultiAlternatives(subject, template_text, 'Cory and Rowena <hello@coryandro.com>', recipients,
                                 reply_to=['hello@coryandro.com'])
    msg.attach_alternative(template_html, "text/html")
    msg.mixed_subtype = 'related'
    for filename in (context['main_image'], ):
        attachment_path = os.path.join(os.path.dirname(__file__), 'static', 'invitation', 'images', filename)
        with open(attachment_path, "rb") as image_file:
            msg_img = MIMEImage(image_file.read())
            msg_img.add_header('Content-ID', '<{}>'.format(filename))
            msg.attach(msg_img)

    print 'sending invitation to {}'.format(', '.join(recipients))
    if not test_only:
        msg.send()
