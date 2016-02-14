from django.dispatch import Signal


tracker_opened = Signal(providing_args=('tracking_category', 'tracking_id'))
