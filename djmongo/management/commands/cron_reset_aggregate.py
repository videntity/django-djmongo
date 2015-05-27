from django.core.management.base import BaseCommand, CommandError, NoArgsCommand
import datetime
import calendar
from djmongo.search.models import Aggregation


class Command(NoArgsCommand):
    help = 'Resetts all aggergations scheduled_job_completed_for_today flags to False. Set this script to run at midnight via cron.'

    def handle_noargs(self, **options): 
        self.stdout.write("Resetting all aggergations scheduled_job_completed_for_today flags to False.")
        
        aggs = Aggregation.objects.all()     
                    
        
        for a in aggs:        
            msg = "Resetting %s" % (a.slug)
            self.stdout.write(msg)
            a.scheduled_job_completed_for_today = False
            a.save()
        self.stdout.write("Reset complete.")
            