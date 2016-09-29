#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.db import models
from django.conf import settings
from ..mongoutils import run_aggregation_pipeline
import json
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Aggregation(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    slug = models.SlugField(max_length=100, unique=True)
    pipeline = models.TextField(max_length=20480, default="[]",
                                verbose_name="Pipeline")
    database_name = models.CharField(max_length=256)
    collection_name = models.CharField(max_length=256)
    output_collection_name = models.CharField(
        max_length=256,
        help_text="""The resulting collection.
        Do not include $out in your pipeline.""")
    creation_date = models.DateField(auto_now_add=True)

    execute_now = models.BooleanField(blank=True, default=False)

    scheduled_job_in_process = models.BooleanField(blank=True, default=False)
    scheduled_job_completed_for_today = models.BooleanField(
        blank=True, default=False)
    scheduled_job_not_ran = models.BooleanField(blank=True, default=True)

    execute_everyday = models.BooleanField(blank=True, default=False)
    execute_sunday = models.BooleanField(blank=True, default=False)
    execute_monday = models.BooleanField(blank=True, default=False)
    execute_tuesday = models.BooleanField(blank=True, default=False)
    execute_wednesday = models.BooleanField(blank=True, default=False)
    execute_thursday = models.BooleanField(blank=True, default=False)
    execute_friday = models.BooleanField(blank=True, default=False)
    execute_saturday = models.BooleanField(blank=True, default=False)
    execute_time_1 = models.TimeField(
        verbose_name="Execute Time",
        help_text="Use 24 hour time. (e.g. 20:30:00 for 8:30 pm)")
    description = models.TextField(max_length=1024, blank=True, default="")

    class Meta:
        get_latest_by = "creation_date"
        ordering = ('-creation_date',)
        verbose_name_plural = "Saved Aggregations"

    def __str__(self):
        return "%s" % (self.slug)

    def save(self, **kwargs):
        if self. execute_everyday:
            self.execute_sunday = True
            self.execute_monday = True
            self.execute_tuesday = True
            self.execute_wednesday = True
            self.execute_thursday = True
            self.execute_friday = True
            self.execute_saturday = True

        super(Aggregation, self).save(**kwargs)

        # Execute now if the flag is set to do so.
        if self.execute_now:
            # Process aggregation
            pipeline = json.loads(self.pipeline)
            output_dict = {"$out": self.output_collection_name}
            pipeline.append(output_dict)
            result = run_aggregation_pipeline(
                self.database_name, self.collection_name, pipeline)
            return result
