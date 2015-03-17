from optparse import make_option
from django.core.management.base import BaseCommand
import traceback

def get_stack_trace():
    return traceback.format_exc()

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--run', action='store_true', dest='run', default=False, help='run'),)

    def handle(self, *args, **options):
        if options['run']:
            run()

def run():
    pass