import base64
import os
import random
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import ListView
from postmark import PMMail
from guests import csv_import
from guests.models import Guest
from guests.save_the_date import get_save_the_date_context, send_save_the_date_email, SAVE_THE_DATE_TEMPLATE, \
    SAVE_THE_DATE_CONTEXT_MAP


class GuestListView(ListView):
    model = Guest


@login_required
def export_guests(request):
    export = csv_import.export_guests()
    response = HttpResponse(export.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=all-guests.csv'
    return response


def invitation(request):
    return render(request, template_name='guests/invitation.html')


def save_the_date_random(request):
    template_id = random.choice(SAVE_THE_DATE_CONTEXT_MAP.keys())
    return save_the_date_preview(request, template_id)


def save_the_date_preview(request, template_id):
    context = get_save_the_date_context(template_id)
    context['email_mode'] = False
    return render(request, SAVE_THE_DATE_TEMPLATE, context=context)


@login_required
def test_email(request, template_id):
    context = get_save_the_date_context(template_id)
    send_save_the_date_email(context, ['cory.zue@gmail.com'])
    # send_save_the_date_email(context, ['cory.zue@gmail.com', 'rowenaluk@gmail.com'])
    return HttpResponse('sent!')


@login_required
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
