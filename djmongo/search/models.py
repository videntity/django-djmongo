from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from django.contrib.auth.models import Group
from ..mongoutils import run_aggregation_pipeline
import json

OUTPUT_CHOICES = (("json","JSON"),
                  ("html", "HTML"),
                  ("csv","Comma Seperated Value (.csv)"),
                  )


class Aggregation(models.Model):

    user            = models.ForeignKey(settings.AUTH_USER_MODEL)
    output_format   = models.CharField(max_length=4, choices=OUTPUT_CHOICES,
                                        default="json")
    
    slug            = models.SlugField(max_length=100, unique=True)
    pipeline        = models.TextField(max_length=20480, default="[]",            
                                        verbose_name="Pipeline")
    
    is_public       =  models.BooleanField(default=False, blank=True,
                            help_text = "If checked, the search can be run without authentication")

    
    sort            =  models.TextField(max_length=2048, default="", blank=True,
                                        verbose_name="Sort Dict",
                                        help_text="""e.g. [["somefield", 1], ["someotherfield", -1] ]""")
    
    return_keys   =  models.TextField(max_length=2048, default="", blank=True,
                                      
                            help_text = "Limit results to these keys.Seperate keys by whitespace. Default is blank, which returns all keys.",
                                        )
    
    default_limit   =  models.IntegerField(default=getattr(settings, 'MONGO_LIMIT', 200),
                            help_text = "Limit results to this number unless specified otherwise.",
                                        )
    database_name   = models.CharField(max_length=256)
    collection_name = models.CharField(max_length=256)
    output_collection_name = models.CharField(max_length=256,
                             help_text = "The resulting collection. Do not include $out in your pipeline.")
    creation_date   = models.DateField(auto_now_add=True)
    execute_now     = models.BooleanField(blank=True, default=False)
    description     = models.TextField(max_length=1024, blank=True, default="")
    
    class Meta:
        get_latest_by = "creation_date"
        ordering = ('-creation_date',)
        verbose_name_plural = "Saved Aggregations"
    def __unicode__(self):
        return "%s" % (self.slug)
        
    def save(self, **kwargs):
       
       #Save off the bat
        super(Aggregation, self).save(**kwargs)
        #Now try and execute
        if self.execute_now:
            #Process aggregation
            print "aggregate"
            pipeline = json.loads(self.pipeline)
            output_dict = {"$out": self.output_collection_name}
            pipeline.append(output_dict)
            result  = run_aggregation_pipeline(self.database_name, self.collection_name, pipeline)
            #Process aggregation
            print result
        
        
        



class SavedSearch(models.Model):

    user            = models.ForeignKey(settings.AUTH_USER_MODEL)
    group           = models.ForeignKey(Group, blank=True, null=True)
    output_format   = models.CharField(max_length=4, choices=OUTPUT_CHOICES,
                                        default="json")
    title           = models.CharField(max_length=100, unique=True)
    slug            = models.SlugField(max_length=100, unique=True)
    query           = models.TextField(max_length=2048, default="{}",            
                                        verbose_name="JSON Query Dict")
    
    is_public       =  models.BooleanField(default=False, blank=True,
                            help_text = "If checked, the search can be run without authentication")
    
    
    
    
    
    sort            =  models.TextField(max_length=2048, default="", blank=True,
                                        verbose_name="Sort Dict",
                                        help_text="""e.g. [["somefield", 1], ["someotherfield", -1] ]""")
    
    return_keys   =  models.TextField(max_length=2048, default="", blank=True,
                                      
                            help_text = "Limit results to these keys.Seperate keys by whitespace. Default is blank, which returns all keys.",
                                        )
    
    default_limit   =  models.IntegerField(default=getattr(settings, 'MONGO_LIMIT', 200),
                            help_text = "Limit results to this number unless specified otherwise.",
                                        )
    database_name   = models.CharField(max_length=100)
    collection_name = models.CharField(max_length=100)
    creation_date   = models.DateField(auto_now_add=True)
    
    class Meta:
        get_latest_by = "creation_date"
        ordering = ('-creation_date',)
        verbose_name_plural = "Saved Searches"

    def __unicode__(self):
        return "%s" % (self.slug)
        
    def save(self, **kwargs):
       
        #Generate the slug if the record it was not already defined.
        if not self.id and not self.slug:
            self.slug = slugify(self.title)
        super(SavedSearch, self).save(**kwargs)
        
        
        
class DatabaseAccessControl(models.Model):

    database_name   = models.CharField(max_length=256)
    collection_name = models.CharField(max_length=256)
    is_public       = models.BooleanField(default=False, blank=True)
    groups          = models.ManyToManyField(Group,  blank=True,
                                related_name = "djmongo_database_access_control")
    
    class Meta:
        #get_latest_by = "creation_date"
        #ordering = ('-creation_date',)
        verbose_name_plural = "Database Access Controls"
        unique_together =  (('database_name','collection_name'), )

    def __unicode__(self):
        return "%s/%s" % (self.database_name, self.collection_name )
        

