from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
from django.contrib.auth.models import Group
from django.core.management import call_command


class Command(NoArgsCommand):
    help = "Creates initial groups for djmongo security groups."

    def handle_noargs(self, **options):
        print "Hello, World!"

#class Command(BaseCommand):
#    help = 'Creates initial groups for djmong security groups.'
#
#    def add_arguments(self, parser):
#        parser.add_argument('poll_id', nargs='+', type=int)
#
#    def handle(self, *args, **options):
#        
#        call_command('loaddata', 'initial_groups.json')
#
#        self.stdout.write('Successfully loaded data.')


