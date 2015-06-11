#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 

from django.conf import settings
import os, json, sys
from pymongo import MongoClient, DESCENDING
from bson.objectid import ObjectId
import csv
from collections import OrderedDict
from ..mongoutils import delete_mongo, write_mongo


def mongo_delete_json_util(database_name, collection_name, query={},
                 just_one=False):
   
   response_dict ={}
   valid_json = True
   try:
      query = json.loads(query, object_pairs_hook=OrderedDict)
      if type(query)!=type(OrderedDict()):
         valid_json = False
   except ValueError:
      valid_json = False

   if valid_json == False:
      response_dict['code']=400
      response_dict['type']="Error"
      response_dict['message']="Your query was not valid JSON or not a dictionary (i.e.{})."
   else:
       #valid json so run the delete
       response_dict = delete_mongo(query, database_name=database_name,
                              collection_name=collection_name, just_one=False)
   
   return response_dict
   
def mongo_create_json_util(document, database_name,
                 collection_name):
   
   response_dict ={}
   valid_json = True
   
   try:
      document = json.loads(document, object_pairs_hook=OrderedDict)
      if type(document)!=type(OrderedDict()):
         valid_json = False
   except ValueError:
      valid_json = False

   if valid_json == False:
      response_dict['code']=400
      response_dict['type']="Error"
      response_dict['message']="Your query was not valid JSON or not a JSON object (i.e.{})."
   else:
       #valid json so run the delete
       response_dict = write_mongo(document,
                                   database_name=database_name,
                                   collection_name=collection_name)
   
   
   return response_dict
   
  
def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]
   

def create_mongo_db(database_name, collection_name, initial_document):
   """create dat new database and collection by inserting one document."""

   response_dict={}
    
   try:
      mc =   MongoClient(host=settings.MONGO_HOST,
                           port=settings.MONGO_PORT)
        
      db          =   mc[str(database_name)]
      collection  =  db[str(collection_name)]
      
      d = json.loads(initial_document, object_pairs_hook=OrderedDict)
      
      myobjectid=collection.save(d)
        
   except:
      #error connecting to mongodb
      response_dict['error']=str(sys.exc_info())
   
   return response_dict



def show_dbs():
   """return a list of all dbs and related collections.
   Return an empty list on error.
   """
    
   #print "skip and limit", skip, limit
   l=[]
   response_dict={}
   try:
      mc =   MongoClient(host=settings.MONGO_HOST,
                           port=settings.MONGO_PORT)
      dbs = mc.database_names()
        
        
      #Hide a couple admin dbs from our UI.
      if "local" in dbs:
         dbs.remove("local")
      if "admin" in dbs:
         dbs.remove("admin")
      for d in dbs:
          dbc =   mc[d]
          collections = dbc.collection_names()  
          collections = remove_values_from_list(collections, "system.indexes")
          l.append({"name":d, "collections":collections})
      return tuple(l)
    
   except:
      #error connecting to mongodb
      print str(sys.exc_info())
      return ()






def mongodb_clear_collection(database_name, collection_name):
    #print """ clear a mongo collection i.e. remove({})"""
    
    l=[]
    response_dict={}
    try:
         mc =   MongoClient(host=settings.MONGO_HOST,
                           port=settings.MONGO_PORT)
         dbs =  mc[database_name]
         dbc =  dbs[collection_name]
        
         dbc.remove({})
         #print "success"
         return ""
    except:
        #error connecting to mongodb
        #print str(sys.exc_info())
        return str(sys.exc_info())




def mongodb_ensure_index(database_name, collection_name, keys):
    """ ensure index """
    
    l=[]
    response_dict={}
    try:
        mc =   MongoClient(host=settings.MONGO_HOST,
                           port=settings.MONGO_PORT)
        dbs =  mc[database_name]
        dbc =  dbs[collection_name]

        dbc.ensure_index(keys)
        #print "success"
        return ""
    
    except:
        #error connecting to mongodb
        #print str(sys.exc_info())
        return str(sys.exc_info())



def mongodb_drop_collection(database_name, collection_name):
    """return a list of all dbs and related collections"""
    
    #print "skip and limit", skip, limit
    l=[]
    response_dict={}
    try:
         mc =   MongoClient(host=settings.MONGO_HOST,
                           port=settings.MONGO_PORT)
         dbs =  mc[database_name]
         dbc =  dbs[collection_name]
         dbs.drop_collection(collection_name)
         #print "success"
         return ""
    
    except:
        #error connecting to mongodb
        #print str(sys.exc_info())
        return str(sys.exc_info())


def mongodb_drop_database(database_name):
    """return a list of all dbs and related collections"""
    
    #print "skip and limit", skip, limit
    l=[]
    response_dict={}
    try:
         mc =   MongoClient(host=settings.MONGO_HOST,
                           port=settings.MONGO_PORT)
         mc.drop_database(database_name)
         #print "success"
         return ""
    
    except:
        #error connecting to mongodb
        #print str(sys.exc_info())
        return str(sys.exc_info())
 