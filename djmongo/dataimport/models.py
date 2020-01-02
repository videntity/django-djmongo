#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.db import models
import os
import uuid
import json
from .utils import bulk_csv_import_mongo


def update_import_filename(instance, filename):
    path = "imports/"
    format = instance.database_name + "-" + \
        instance.collection_name  + "-" + \
        str(uuid.uuid4())[0:5] + "-" + filename
    return os.path.join(path, format)


INPUT_CHOICES = (("csv", "Comma Separated Value (.csv)"),)


class DataImport(models.Model):

    file1 = models.FileField(upload_to=update_import_filename,
                             verbose_name="File to be Imported")
    input_format = models.CharField(max_length=3,
                                    choices=INPUT_CHOICES,
                                    default="csv")

    delete_collection_before_import = models.BooleanField(default=False)

    status = models.CharField(max_length=10,
                              default="New",
                              verbose_name="Status", editable=False)

    response = models.TextField(max_length=2048, default="", blank=True,
                                verbose_name="Response")

    database_name = models.CharField(max_length=256)

    collection_name = models.CharField(max_length=256)

    creation_date = models.DateField(auto_now_add=True)

    class Meta:
        get_latest_by = "creation_date"
        ordering = ('-creation_date',)

    def __str__(self):
        return "%s/%s" % (self.database_name, self.collection_name)

    def save(self, commit=True, **kwargs):
        self.status = "Processing"

        # Generate the slug if the record it was not already defined.
        super(DataImport, self).save(**kwargs)
        # process the file
        result = bulk_csv_import_mongo(self.file1,
                                       self.database_name,
                                       self.collection_name,
                                       self.delete_collection_before_import)

        print(result)
        # report results
        self.response = json.dumps(result, indent=4)
        self.status = "Complete"
        # re-write db after complete
        if commit:
            super(DataImport, self).save(**kwargs)
