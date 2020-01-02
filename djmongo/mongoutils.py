#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django.conf import settings
import json
import sys
import csv
from datetime import datetime, date, time
from bson.code import Code
from bson.objectid import ObjectId
from bson.errors import InvalidId
from bson import json_util
from pymongo import MongoClient, DESCENDING
from collections import OrderedDict


def checkObjectId(s):
    try:
        ObjectId(s)
    except InvalidId:
        return False
    return True


def run_aggregation_pipeline(database_name, collection_name, pipeline):
    result = False
    mongodb_client_url = getattr(settings, 'MONGODB_CLIENT',
                                 'mongodb://localhost:27017/')
    mc = MongoClient(mongodb_client_url)
    db = mc[str(database_name)]
    collection = db[str(collection_name)]

    # explain = db.command('aggregate', collection, pipeline=pipeline, explain=True)
    # print explain
    collection.aggregate(pipeline)

    # print agg_result
    result = True
    return result


def to_json(results_dict):
    return json.dumps(results_dict, indent=4, default=json_util.default)


def normalize_results(results_dict):
    mydt = datetime.now()
    myd = date.today()
    myt = time(0, 0)

    for r in results_dict['results']:
        for k, v in r.items():
            if isinstance(r[k], type(mydt)) or \
               isinstance(r[k], type(myd)) or \
               isinstance(r[k], type(myt)):
                r[k] = v.__str__()
                # print r[k]
    return results_dict


def normalize_list(results_list):
    mydt = datetime.now()
    for r in results_list:
        for k, v in r.items():
            if isinstance(r[k], type(mydt)):
                r[k] = v.__str__()
    return results_list


def query_mongo(
        database_name,
        collection_name,
        query={},
        include_num_results="0",
        skip=0,
        sort=None,
        limit=getattr(
            settings,
            'MONGO_LIMIT',
            200),
        cast_strings_to_integers=False,
        return_keys=()):
    """return a response_dict  with a list of search results"""

    l = []
    response_dict = {}

    try:
        mongodb_client_url = getattr(settings, 'MONGODB_CLIENT',
                                     'mongodb://localhost:27017/')
        mc = MongoClient(mongodb_client_url, document_class=OrderedDict)

        db = mc[str(database_name)]
        collection = db[str(collection_name)]

        # Cast the query to integers
        if cast_strings_to_integers:
            query = cast_number_strings_to_integers(query)

        # print query
        if return_keys:
            return_dict = {}
            for k in return_keys:
                return_dict[k] = 1
            # print "returndict=",return_dict
            mysearchresult = collection.find(
                query, return_dict).skip(skip).limit(limit)
        else:
            mysearchresult = collection.find(query).skip(skip).limit(limit)

        if sort:
            mysearchresult.sort(sort)

        response_dict['code'] = 200
        if include_num_results == "1":
            response_dict['num_results'] = response_dict['num_results'] = int(
                mysearchresult.count(with_limit_and_skip=False))

        if include_num_results == "2":
            response_dict['num_results'] = response_dict['num_results'] = int(
                mysearchresult.count(with_limit_and_skip=True))

        response_dict['type'] = "search-results"
        for d in mysearchresult:
            d['id'] = d['_id'].__str__()
            del d['_id']
            l.append(d)
        response_dict['results'] = l

    except:
        print("Error reading from Mongo")
        print(str(sys.exc_info()))
        response_dict['num_results'] = 0
        response_dict['code'] = 500
        response_dict['type'] = "Error"
        response_dict['results'] = []
        response_dict['message'] = str(sys.exc_info())

    return response_dict


def query_mongo_sort_decend(
        database_name,
        collection_name,
        query={},
        skip=0,
        limit=getattr(
            settings,
            'MONGO_LIMIT',
            200),
    return_keys=(),
        sortkey=None):
    """return a response_dict  with a list of search results in decending
    order based on a sort key
    """

    l = []
    response_dict = {}

    try:
        mongodb_client_url = getattr(settings, 'MONGODB_CLIENT',
                                     'mongodb://localhost:27017/')
        mc = MongoClient(mongodb_client_url, document_class=OrderedDict)

        db = mc[str(database_name)]
        collection = db[str(collection_name)]

        if return_keys:
            return_dict = {}
            for k in return_keys:
                return_dict[k] = 1
            # print "returndict=",return_dict
            mysearchresult = collection.find(
                query, return_dict).skip(skip).limit(limit).sort(
                sortkey, DESCENDING)
        else:
            mysearchresult = collection.find(query).skip(
                skip).limit(limit).sort(sortkey, DESCENDING)

        # response_dict['num_results']=int(mysearchresult.count(with_limit_and_skip=False))
        response_dict['code'] = 200
        response_dict['type'] = "search-results"
        for d in mysearchresult:
            d['id'] = d['_id'].__str__()
            del d['_id']
            l.append(d)
        response_dict['results'] = l

    except:
        print("Error reading from Mongo")
        print(str(sys.exc_info()))
        response_dict['num_results'] = 0
        response_dict['code'] = 500
        response_dict['type'] = "Error"
        response_dict['results'] = []
        response_dict['message'] = str(sys.exc_info())
    return response_dict


def delete_mongo(database_name, collection_name,
                 query={}, just_one=False):
    """delete from mongo helper"""

    l = []
    response_dict = {}

    try:
        mongodb_client_url = getattr(settings, 'MONGODB_CLIENT',
                                     'mongodb://localhost:27017/')
        mc = MongoClient(mongodb_client_url, document_class=OrderedDict)
        db = mc[str(database_name)]
        collection = db[str(collection_name)]

        mysearchresult = collection.remove(query, just_one)

        response_dict['code'] = 200
        response_dict['type'] = "remove-confirmation"

    except:
        # print "Error reading from Mongo"
        # print str(sys.exc_info())
        response_dict['num_results'] = 0
        response_dict['code'] = 500
        response_dict['type'] = "Error"
        response_dict['results'] = []
        response_dict['message'] = str(sys.exc_info())
    return response_dict


def write_mongo(document, database_name,
                collection_name, update=False):
    """Write a document to the collection. Return a response_dict containing
    the written record. Method functions as both insert or update based on update
    parameter"""

    l = []
    response_dict = {}
    try:
        mongodb_client_url = getattr(settings, 'MONGODB_CLIENT',
                                     'mongodb://localhost:27017/')
        mc = MongoClient(mongodb_client_url, document_class=OrderedDict)
        db = mc[str(database_name)]
        collection = db[str(collection_name)]

        # Cast the query to integers
        # if settings.CAST_ININGS_TO_INTEGERS:
        #    query = cast_number_strings_to_integers(query)

        potential_key_found = False
        existing_transaction_id = None
        existing_mongo_id = None

        # enforce non-repudiation constraint on create
        # if document.has_key("transaction_id"):
        #    existing_transaction_id = collection.find_one({'transaction_id':document['transaction_id']})
        #    if existing_transaction_id:
        #        potential_key_found = True

        if "id" in document:
            document["_id"] = ObjectId(document["id"])
            del document["id"]

        if "_id" in document:
            existing_mongo_id = collection.find_one({'_id': document['_id']})
            if existing_mongo_id:
                potential_key_found = True

        if update == False and potential_key_found == True:
            """409 conflict"""
            response_dict['code'] = 409
            response_dict['type'] = "Error"
            response_dict['results'] = []
            response_dict[
                'message'] = "Perhaps you meant to perform an update instead?"
            response_dict['errors'] = [
                "Conflict. This transaction_id has already been created.", ]
            return response_dict

        elif update and potential_key_found:  # this is an update
            # set kwargs _id to the existing_id to force to overwrite existing
            # document

            # if existing_transaction_id:
            #
            #    document['_id'] = ObjectId(existing_transaction_id['_id'])
            #    document['history']=True
            #    history_collection_name = "%s_history" % str(collection_name)
            #    history_collection   = db[str(history_collection_name)]
            #
            #    history_object = existing_transaction_id
            #    history_object['historical_id'] = existing_transaction_id['_id']
            #    del history_object['_id']
            #    #now write the record to the historical collection
            #    written_object = history_collection.insert(history_object)

            if existing_mongo_id:
                document['_id'] = ObjectId(existing_mongo_id['_id'])
                document['history'] = True
                history_collection_name = "%s_history" % str(collection_name)
                history_collection = db[str(history_collection_name)]

                # print history_collection
                # print existing_mongo_id

                history_object = existing_mongo_id

                history_object['historical_id'] = existing_mongo_id['_id']
                del history_object['_id']
                # print history_object

                # now write the record to the historical collection
                written_object = history_collection.insert(history_object)

            # update the record
            myobjectid = collection.save(document)

        else:
            # this is new so perform an insert.
            myobjectid = collection.insert(document)

        # now fetch the record we just wrote so that we write it back to the
        # DB.
        myobject = collection.find_one({'_id': myobjectid})
        response_dict['code'] = 200
        response_dict['type'] = "write-results"
        myobject['id'] = myobject['_id'].__str__()
        del myobject['_id']
        l.append(myobject)
        response_dict['results'] = l

    except:
        # print "Error reading from Mongo"
        # print str(sys.exc_info())
        response_dict['code'] = 400
        response_dict['type'] = "Error"
        response_dict['results'] = []
        response_dict['message'] = str(sys.exc_info())
    return response_dict


def bulk_csv_import_mongo(csvfile, database_name, collection_name,
                          delete_collection_before_import=False):
    """return a response_dict  with a list of search results"""
    """method can be insert or update"""

    l = []
    response_dict = {}
    try:
        mongodb_client_url = getattr(settings, 'MONGODB_CLIENT',
                                     'mongodb://localhost:27017/')
        mc = MongoClient(mongodb_client_url, document_class=OrderedDict)
        db = mconnection[database_name]
        collection = db[collection_name]

        if delete_collection_before_import:
            myobjectid = collection.remove({})

        # open the csv file.
        csvhandle = csv.reader(open(csvfile._get_path(), 'rb'), delimiter=',')

        rowindex = 0
        errors = 0
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
                    cleaned_headers.append(c)
            else:

                record = OrderedDict(zip(cleaned_headers, row))
                # if there is no values, skip the key value pair
                kwargs = OrderedDict()

                # Only populate fields that are not blank.
                for k, v in record.items():
                    if v:
                        if v.isdigit():
                            kwargs[k] = int(v)
                        else:
                            kwargs[k] = v
                try:

                    myobjectid = collection.insert(kwargs)
                    success += 1
                except:
                    error_message = "Error on row " + \
                        rowindex + ". " + str(sys.exc_info())
                    error_list.append(str(sys.exc_info()))

            rowindex += 1

        if error_list:
            response_dict = {}
            response_dict['num_rows_imported'] = rowindex
            response_dict['num_rows_errors'] = len(error_list)
            response_dict['errors'] = error_list
            response_dict['code'] = 400
            response_dict['message'] = "Completed with errors"
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


def build_non_observational_key(k):

    if str(k).__contains__("__"):
        model_field_split = str(k).split("__")
        newlabel = "%s_" % (model_field_split[0])

        field_occurence_split = str(model_field_split[1]).split("_")

        for i in field_occurence_split[:-1]:
            newlabel = "%s_%s" % (newlabel, i)
        return newlabel
    return k


def get_collection_keys(database_name, collection_name):
    l = []
    try:
        mongodb_client_url = getattr(settings, 'MONGODB_CLIENT',
                                     'mongodb://localhost:27017/')
        mc = MongoClient(mongodb_client_url, document_class=OrderedDict)
        db = mconnection[database_name]
        ckey_collection = "%s_keys" % (collection_name)
        collection = db[ckey_collection]
        result = collection.find({}).distinct("_id")
        for r in result:
            l.append(r)

        if getattr(settings, 'SORTCOLUMNS', False):
            nl = []  # new list list
            # sort the list according to our list

            for i in getattr(settings, 'SORTCOLUMNS', False):
                for j in l:
                    if j.__contains__(i):
                        nl.append(j)
            difflist = list(set(l) - set(nl))

            for i in difflist:
                nl.append(i)
            return nl

        else:
            return sorted(l)
    except:
        print("Error.", str(sys.exc_info()))
        return []


def build_keys_with_mapreduce(database_name, collection_name):
    map = Code("function() { "
               "    for (var key in this)"
               "        { emit(key, null); } }"
               )
    reduce = Code("function(key, stuff)"
                  "{ return null; }"
                  )

    mongodb_client_url = getattr(settings, 'MONGODB_CLIENT',
                                 'mongodb://localhost:27017/')
    mc = MongoClient(mongodb_client_url, document_class=OrderedDict)
    db = mc[database_name]

    collection = db[collection_name]
    result_collection_name = "%s_keys" % (collection_name)

    result = collection.map_reduce(map, reduce, result_collection_name)
    return None


def raw_query_mongo_db(kwargs, database_name, collection_name):
    # for key in kwargs:
    #    print "arg: %s: %s" % (key, kwargs[key])
    """return a result list or an empty list"""
    l = []
    response_dict = {}

    try:
        mongodb_client_url = getattr(settings, 'MONGODB_CLIENT',
                                     'mongodb://localhost:27017/')
        mc = MongoClient(mongodb_client_url, document_class=OrderedDict)
        db = mc[database_name]
        transactions = db[collection_name]
        mysearchresult = transactions.find(kwargs)
        mysearchcount = mysearchresult.count()
        if mysearchcount > 0:
            response_dict['code'] = 200
            for d in mysearchresult:
                l.append(d)
            response_dict['results'] = l
    except:
        # print "Error reading from Mongo"
        # print str(sys.exc_info())
        response_dict['code'] = 400

        response_dict['type'] = "Error"
        response_dict['message'] = str(sys.exc_info())
    return response_dict


def cast_number_strings_to_integers(d):
    """d is a dict"""
    for k, v in d.items():
        # print type(v)
        if determine_if_str_or_unicode(v):
            if v.isdigit():
                d[k] = int(v)
    return d


def determine_if_str_or_unicode(s):
    # if str or unicode return True, else False.
    if isinstance(s, str) or isinstance(s, unicode):
        return True
    return False
