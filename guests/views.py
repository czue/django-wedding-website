import base64
from email.mime.image import MIMEImage
import os
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from django.views.generic import ListView, TemplateView
from postmark import PMMail
from guests.models import Guest


class GuestListView(ListView):
    model = Guest


class RoEmailPreviewView(TemplateView):
    template_name = 'guests/email_templates/save_the_date_ro.html'

    def get_context_data(self, **kwargs):
        return {
            'header_filename': 'hearts.png'
        }


class CoryEmailPreviewView(TemplateView):
    template_name = 'guests/email_templates/save_the_date_cory.html'

    def get_context_data(self, **kwargs):
        return {
            'header_filename': 'maple-leaf.png'
        }


def test_email(request):
    template_html = render_to_string('guests/email_templates/save_the_date_ro.html', context={'email_mode': True})
    template_text = 'sorry, you need to view this in html mode'
    subject = 'save the date!'
    recipients = ['cory.zue@gmail.com']
    # https://www.vlent.nl/weblog/2014/01/15/sending-emails-with-embedded-images-in-django/
    msg = EmailMultiAlternatives(subject, template_text, 'hello@coryandro.com', recipients)
    msg.attach_alternative(template_html, "text/html")
    msg.mixed_subtype = 'related'
    for filename in ('hearts.png', 'selfie.jpg'):
        attachment_path = os.path.join(os.path.dirname(__file__), 'static', 'save-the-date', 'images', filename)
        with open(attachment_path, "rb") as image_file:
            msg_img = MIMEImage(image_file.read())
            msg_img.add_header('Content-ID', '<{}>'.format(filename))
            msg.attach(msg_img)

    msg.send()
    return HttpResponse('sent!')
    # return HttpResponseRedirect(reverse('save-the-date'))


def test_postmark_email(request):
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


def _base64_encode(filepath):
    with open(filepath, "rb") as image_file:
        return base64.b64encode(image_file.read())
