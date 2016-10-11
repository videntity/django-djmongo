#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.core.management.base import NoArgsCommand
from djmongo.aggregations.models import Aggregation


class Command(NoArgsCommand):
    help = 'Resets all aggregations scheduled_job_completed_for_today' \
           'flags to False. Set this script to run at midnight via cron.'

    def handle_noargs(self, **options):
        self.stdout.write(
            "Resetting all aggregations scheduled_job_completed_for_today "
            "flags to False.")
        aggs = Aggregation.objects.all()
        for a in aggs:
            msg = "Resetting %s" % (a.slug)
            self.stdout.write(msg)
            a.scheduled_job_completed_for_today = False
            a.save()
        self.stdout.write("Reset complete.")
