from django.core.management.base import BaseCommand

from cqrs_ddp.ddp_client import DdpCmd


class Command(BaseCommand):
    help = 'Monitor DDP Connection for changes to the Edits Collection Documents'
    args = 'ddp_endpoint'
    option_list = BaseCommand.option_list + (
        make_option(
            '--print-raw',
            dest='print_raw',
            default=False,
            action="store_true",
            help='print raw websocket data'),
        )

    def handle(self, *args, **options):

        print 'ddp_endpoint: %s' % args['ddp_endpoint']
        print 'print_raw' % options['print_raw']

        # app = App(args['ddp_endpoint'], options['print_raw'])
        # try:
        #     app.cmdloop()
        # except KeyboardInterrupt:
        #     # On Ctrl-C or thread.interrupt_main(), just exit without printing a
        #     # traceback.
        #     pass