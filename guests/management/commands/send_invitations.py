from django.core.management import BaseCommand

from guests.invitation import send_all_invitations


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--send',
            action='store_true',
            dest='send',
            default=False,
            help="Actually send emails"
        )
        parser.add_argument(
            '--mark-sent',
            action='store_true',
            dest='mark_sent',
            default=False,
            help="Mark as sent"
        )
        parser.add_argument(
            '--resend-unopened',
            action='store_true',
            dest='unopened',
            default=False,
            help="Mark as sent"
        )

    def handle(self, *args, **options):
        send_all_invitations(test_only=not options['send'], mark_as_sent=options['mark_sent'], unopened=options['unopened'])
