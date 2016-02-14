from django.http import HttpResponse
from .signals import tracker_opened


def track_open(request, tracking_category, tracking_id):
    tracker_opened.send('view', tracking_category=tracking_category, tracking_id=tracking_id)
    return HttpResponse('sent!')
