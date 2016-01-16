import base64
import os
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.views.generic import ListView, TemplateView
from postmark import PMMail
from guests.models import Guest


class GuestListView(ListView):
    model = Guest


class EmailPreviewView(TemplateView):
    template_name = 'guests/email_templates/save_the_date.html'


def test_email(request):
    template_text = render_to_string('guests/email_templates/save_the_date.html', context={'email_mode': True})
    attachments = []
    for filename in ('hearts.png', 'selfie.jpg'):
        attachment_path = os.path.join(os.path.dirname(__file__), 'static', 'save-the-date', 'images', filename)
        encoded_attachment = _base64_encode(attachment_path)
        attachments.append(
            (filename, encoded_attachment, 'image/{}'.format(filename.split('.')[-1]), 'cid:{}'.format(filename))
        )

    mail = PMMail(
        to='Cory Zue <cory.zue@gmail.com>',
        subject='save the date!',
        html_body=template_text,
        text_body='sorry, you need to view this in html mode',
        attachments=attachments
    )
    mail.send()
    return HttpResponseRedirect(reverse('save-the-date'))


def _base64_encode(file_path):
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read())
