from django.views.generic import ListView, TemplateView
from guests.models import Guest


class GuestListView(ListView):
    model = Guest


class EmailPreviewView(TemplateView):
    template_name = 'guests/email_templates/save_the_date.html'

