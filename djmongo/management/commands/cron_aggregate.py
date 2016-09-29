#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.core.management.base import NoArgsCommand
import datetime
import calendar
import json
from djmongo.aggregations.models import Aggregation
from djmongo.mongoutils import run_aggregation_pipeline


class Command(NoArgsCommand):
    help = 'Check for aggregate jobs that have not run. ' \
           'Add this to your crontab to execute every 5 ' \
           'minutes or so.'

    def handle_noargs(self, **options):
        now = datetime.datetime.now()
        now_time = datetime.datetime.time(datetime.datetime.now())
        out = "It is now %s on %s " % (
            now_time, calendar.day_name[now.weekday()])
        weekday = calendar.day_name[now.weekday()]
        self.stdout.write(out)

        if weekday == "Sunday":
            aggs = Aggregation.objects.filter(
                execute_sunday=True,
                execute_time_1__lte=now_time,
                scheduled_job_in_process=False,
                scheduled_job_completed_for_today=False)
        if weekday == "Monday":
            aggs = Aggregation.objects.filter(
                execute_monday=True,
                execute_time_1__lte=now_time,
                scheduled_job_in_process=False,
                scheduled_job_completed_for_today=False)
        if weekday == "Tuesday":
            aggs = Aggregation.objects.filter(
                execute_tuesday=True,
                execute_time_1__lte=now_time,
                scheduled_job_in_process=False,
                scheduled_job_completed_for_today=False)
        if weekday == "Wednesday":
            aggs = Aggregation.objects.filter(
                execute_wednesday=True,
                execute_time_1__lte=now_time,
                scheduled_job_in_process=False,
                scheduled_job_completed_for_today=False)
        if weekday == "Thursday":
            aggs = Aggregation.objects.filter(
                execute_thursday=True,
                execute_time_1__lte=now_time,
                scheduled_job_in_process=False,
                scheduled_job_completed_for_today=False)
        if weekday == "Friday":
            aggs = Aggregation.objects.filter(
                execute_friday=True,
                execute_time_1__lte=now_time,
                scheduled_job_in_process=False,
                scheduled_job_completed_for_today=False)
        if weekday == "Saturday":
            aggs = Aggregation.objects.filter(
                execute_saturday=True,
                execute_time_1__lte=now_time,
                scheduled_job_in_process=False,
                scheduled_job_completed_for_today=False)

        if aggs.count() == 0:
            print("No jobs to run right now")

        for a in aggs:
            msg = "Run job %s" % (a.slug)

            a.scheduled_job_in_process = True
            a.save()
            self.stdout.write(msg)

            # Perform the aggregation
            pipeline = json.loads(a.pipeline)
            output_dict = {"$out": a.output_collection_name}
            pipeline.append(output_dict)
            run_aggregation_pipeline(a.database_name, a.collection_name,
                                     pipeline)

            # Mark it as complete and no longer in process.
            a.scheduled_job_completed_for_today = True
            a.scheduled_job_in_process = False
            a.save()
            msg = "Job %s completed." % (a.slug)
            print(msg)
