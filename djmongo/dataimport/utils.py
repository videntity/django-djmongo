#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django.conf import settings
import csv
import sys
from pymongo import MongoClient
from collections import OrderedDict


def bulk_csv_import_mongo(csvfile, database_name, collection_name,
                          delete_collection_before_import=False):
    """return a response_dict  with a list of search results"""
    """method can be insert or update"""

    response_dict = {}
    try:
        mongodb_client_url = getattr(settings, 'MONGODB_CLIENT',
                                     'mongodb://localhost:27017/')
        mc = MongoClient(mongodb_client_url, document_class=OrderedDict)
        db = mc[str(database_name)]
        collection = db[str(collection_name)]

        if delete_collection_before_import:
            collection.remove({})

        # open the csv file.
        # print(csvfile, dir(csvfile))
        csvhandle = csv.reader(open(csvfile.path, 'r'),
                               delimiter=',')

        rowindex = 0
        error_list = []
        success = 0
        for row in csvhandle:

            if rowindex == 0:
                column_headers = row
                cleaned_headers = []
                for c in column_headers:
                    c = c.replace(".", "")
                    c = c.replace("$", "-")
                    c = c.replace(" ", "_")
                    c = c.replace('"', "")
                    cleaned_headers.append(c)
            else:

                record = dict(zip(cleaned_headers, row))
                # if there is no values, skip the key value pair
                kwargs = OrderedDict()

                # Only populate fields that are not blank.
                for k, v in record.items():
                    if v:
                        kwargs[k] = v
                try:

                    collection.insert(kwargs)
                    success += 1
                except:
                    error_message = "Error on row " + \
                        rowindex + ". " + str(sys.exc_info())
                    error_list.append(error_message)

            rowindex += 1

        if error_list:
            response_dict = {}
            response_dict['num_rows_imported'] = rowindex
            response_dict['num_rows_errors'] = len(error_list)
            response_dict['errors'] = error_list
            response_dict['code'] = 400
            response_dict['message'] = "Completed with errors."
        else:

            response_dict = {}
            response_dict['num_rows_imported'] = success
            response_dict['code'] = 200
            response_dict['message'] = "Completed."
        return response_dict

    except:
        # print "Error reading from Mongo"
        # print str(sys.exc_info())
        response_dict['num_results'] = 0
        response_dict['code'] = 400
        response_dict['type'] = "Error"
        response_dict['results'] = []
        response_dict['message'] = str(sys.exc_info())
    return response_dict
