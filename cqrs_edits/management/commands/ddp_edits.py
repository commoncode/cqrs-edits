from optparse import make_option
from django.core.management.base import BaseCommand

from cqrs_ddp.ddpcmd import DdpCmd


class Command(BaseCommand):
    help = 'Monitor DDP Connection for changes to the Edits Collection Documents'
    args = '<ddp_endpoint>'
    option_list = BaseCommand.option_list + (
        make_option(
            '--print-raw',
            dest='print_raw',
            default=False,
            action="store_true",
            help='print raw websocket data'),
        )

    def handle(self, *args, **options):

        app = DdpCmd([a for a in args][0], options['print_raw'])
        try:
            app.cmdloop()
        except KeyboardInterrupt:
            # On Ctrl-C or thread.interrupt_main(), just exit without printing a
            # traceback.
            pass