#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.utils.datastructures import SortedDict
from django.http import HttpResponse
from datetime import datetime
import csv, string
from ..mongoutils import get_collection_keys, get_collection_labels, build_non_observational_key

def flatten_results(keylist, listresults, exclude=()):

    #print "keylist", keylist
    #print listresults
    #create a blank list to use as our table
    rows =[]
    #if settings.OTHER_LABELS:
    #    labeldict = get_collection_labels()
    #else:
    #    labeldict={}

    # Make the first row
    row=SortedDict()
    for i in keylist:
        row[i]=i
    rows.append(row)
    #print "results", len(listresults)
    #write the rest of the rows.
    for i in listresults:
        #Make the other rows
        row=SortedDict()
        for j in keylist:
            if i.has_key(j):
                
                #print i[j]
                
                if i[j]:
                    if type(i[j])==type([]) or type(i[j])==type({}) :
                        row[j]=str(i[j])
                    else:
                         # Avoiding int object has no attribute encode
                        if isinstance(i[j],(int, long)):
                            row[j] =str(i[j])
                        else:
                            row[j] ="".join(s for s in i[j].encode("ascii", errors="ignore") if s in string.printable)
                else:
                    row[j]=""
            else:
                row[j]=""
        rows.append(row)

    return rows

def tupleize(rows):
    """Also alphabetizes columns and returns a tuple of tuples"""

    #define a blank list as our return object
    l = []
    for r in rows:
        row=[]
        row =list(r.values())
        l.append(row)


    # alphabetize
    if settings.ALPHABETIZE_COLUMNS:
        col = zip(*l)
        col.sort()
        result = zip(*col)
        return result
    else:
        return l


#def apply_custom_labels(rows):
#    if settings.OTHER_LABELS:
#        labeldict = get_collection_labels()
#        counter=0
#        old_column_header = rows[0]
#        new_column_header = []
#        for i in old_column_header:
#            try:
#                l =  DataLabelMeta.objects.get(variable_name = build_non_observational_key(i))
#                new_column_header.append(str(l.label))
#            except(DataLabelMeta.DoesNotExist):
#                #there is no custom label defined, so lets try and use the
#                #regular label from the Data dictionary.
#                if labeldict.has_key(i):
#                    new_column_header.append(labeldict[i])
#                else:
#                    # else, fallback to the system key
#                    new_column_header.append(i)
#        rows[0] = new_column_header
#    return rows


def sort_by_columns(rows):

    if settings.SORTCOLUMNS:
        ncolumns =[]
        columns = list(zip(*rows))
        sl = get_collection_keys()

        for s in sl:
            for c in columns:
                if c[0]==s:
                    ncolumns.append(c)

        difflist = list(set(columns) - set(ncolumns))


        for i in difflist:
            ncolumns.append(i)
        rows = zip(*ncolumns)
        lrows =[]
        for r in rows:
            lrows.append(list(r))
        return lrows

    return rows


def convert_to_xls(keylist, listresults, exclude=()):
    rows = flatten_results(keylist, listresults, exclude=())


    #turn rows into a tuple of tuples
    rows = tupleize(rows)

    if settings.SORTCOLUMNS:
        #sort by our preferred column order, if specificed
        rows = sort_by_columns(rows)



    filename = datetime.now().strftime('%m-%d-%Y_%H:%M:%S') + '.xls'
    response = HttpResponse(mimetype="application/vnd.ms-excel")
    response['Content-Disposition'] = 'attachment; filename=' + filename
    excelwb = excelify(rows)
    excelwb.save(response)
    return response



def convert_labels_to_xls(rows):

    filename = datetime.now().strftime('%m-%d-%Y_%H:%M:%S') + '.xls'
    response = HttpResponse(mimetype="application/vnd.ms-excel")
    response['Content-Disposition'] = 'attachment; filename=' + filename
    excelwb = excelify(rows['labels'])
    excelwb.save(response)
    return response

def convert_to_csv(keylist, listresults, exclude=()):
    rows =flatten_results(keylist, listresults, exclude=())
    rows = tupleize(rows)

    if settings.SORTCOLUMNS:
        #sort by our preferred column order, if specificed
        rows = sort_by_columns(rows)


    filename = datetime.now().strftime('%m-%d-%Y_%H:%M:%S') + '.csv'
    response = HttpResponse(mimetype="text/csv")
    response['Content-Disposition'] = 'attachment; filename=' + filename


    writer = csv.writer(response, delimiter=',')
    for r in rows:
        #filtered_string = "".join(s for s in c if s in string.printable)
        writer.writerows([r])
    return response

def convert_to_rows(keylist, listresults, exclude=()):
    rows =flatten_results(keylist, listresults, exclude=())
    rows = tupleize(rows)

    if settings.SORTCOLUMNS:
        #sort by our preferred column order, if specificed
        rows = sort_by_columns(rows)

    return rows

