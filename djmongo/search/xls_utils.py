#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
from django.conf import settings
from django.http import HttpResponse
from datetime import datetime
from collections import OrderedDict
import csv
import string
from ..mongoutils import get_collection_keys


def flatten_results(keylist, listresults, exclude=()):

    # create a blank list to use as our table
    rows = []
    # Make the first row
    row = OrderedDict()
    for i in keylist:
        row[i] = i
    rows.append(row)

    # write the rest of the rows.
    for i in listresults:
        # Make the other rows
        row = OrderedDict()
        for j in keylist:
            if j in i:

                # print i[j]

                if i[j]:
                    if isinstance(i[j], type([])) or \
                       isinstance(i[j], type({})) or \
                       isinstance(i[j], type(OrderedDict())):
                        row[j] = str(i[j])
                    else:
                        # Avoiding int object has no attribute encode
                        if isinstance(i[j], (int, long, float)):
                            row[j] = str(i[j])
                        else:
                            row[j] = "".join(
                                s for s in i[j].encode(
                                    "ascii", errors="ignore") if s in string.printable)
                else:
                    row[j] = ""
            else:
                row[j] = ""
        rows.append(row)

    return rows


def tupleize(
    rows,
    alphabetize_columns=getattr(
        settings,
        'ALPHABETIZE_COLUMNS',
        False)):
    """Also alphabetizes columns and returns a tuple of tuples"""

    # define a blank list as our return object
    l = []
    for r in rows:
        row = []
        row = list(r.values())
        l.append(row)

    # alphabetize
    if alphabetize_columns:
        col = sorted(zip(*l))
        result = zip(*col)
        return result
    else:
        return l


def sort_by_columns(
    rows,
    sort_columns=getattr(
        settings,
        'SORTCOLUMNS',
        False)):

    if sort_columns:
        ncolumns = []
        columns = list(zip(*rows))
        sl = get_collection_keys()

        for s in sl:
            for c in columns:
                if c[0] == s:
                    ncolumns.append(c)

        difflist = list(set(columns) - set(ncolumns))

        for i in difflist:
            ncolumns.append(i)
        rows = zip(*ncolumns)
        lrows = []
        for r in rows:
            lrows.append(list(r))
        return lrows

    return rows


def convert_to_csv(keylist, listresults, exclude=(),
                   sort_columns=getattr(settings, 'SORTCOLUMNS', False)):
    rows = flatten_results(keylist, listresults, exclude=())
    rows = tupleize(rows)

    if sort_columns:
        # sort by our preferred column order, if specificed
        rows = sort_by_columns(rows)

    filename = datetime.now().strftime('%m-%d-%Y_%H:%M:%S') + '.csv'
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename=' + filename

    writer = csv.writer(response, delimiter=',')
    for r in rows:
        # filtered_string = "".join(s for s in c if s in string.printable)
        writer.writerows([r])
    return response


def convert_to_rows(keylist, listresults, exclude=(),
                    sort_columns=getattr(settings, 'SORTCOLUMNS', False)):
    rows = flatten_results(keylist, listresults, exclude=())
    rows = tupleize(rows)

    if sort_columns:
        # sort by our preferred column order, if specificed
        rows = sort_by_columns(rows)

    return rows
