from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from django.contrib.auth.models import Group
from ..mongoutils import run_aggregation_pipeline
import json
from django.utils.encoding import python_2_unicode_compatible

OUTPUT_CHOICES = (("json","JSON"),
                  ("html", "HTML"),
                  ("csv","Comma Seperated Value (.csv)"),
                  )

@python_2_unicode_compatible
class Aggregation(models.Model):

    user            = models.ForeignKey(settings.AUTH_USER_MODEL)

    slug            = models.SlugField(max_length=100, unique=True)
    pipeline        = models.TextField(max_length=20480, default="[]",            
                                        verbose_name="Pipeline")
    database_name   = models.CharField(max_length=256)
    collection_name = models.CharField(max_length=256)
    output_collection_name = models.CharField(max_length=256,
                             help_text = "The resulting collection. Do not include $out in your pipeline.")
    creation_date          = models.DateField(auto_now_add=True)
    
    execute_now            = models.BooleanField(blank=True, default=False)
    
    scheduled_job_in_process      = models.BooleanField(blank=True, default=False)
    scheduled_job_completed_for_today       = models.BooleanField(blank=True, default=False)
    scheduled_job_not_ran         = models.BooleanField(blank=True, default=True)
    
    execute_everyday  = models.BooleanField(blank=True, default=False)
    execute_sunday    = models.BooleanField(blank=True, default=False)
    execute_monday    = models.BooleanField(blank=True, default=False)
    execute_tuesday   = models.BooleanField(blank=True, default=False)
    execute_wednesday = models.BooleanField(blank=True, default=False)
    execute_thursday  = models.BooleanField(blank=True, default=False)
    execute_friday    = models.BooleanField(blank=True, default=False)
    execute_saturday  = models.BooleanField(blank=True, default=False)
    execute_time_1    = models.TimeField(help_text = "Use 24 hour time. (e.g. 20:30:00 for 8:30 pm)")
    description       = models.TextField(max_length=1024, blank=True, default="")
    
    class Meta:
        get_latest_by = "creation_date"
        ordering = ('-creation_date',)
        verbose_name_plural = "Saved Aggregations"
    def __str__(self):
        return "%s" % (self.slug)
        
    def save(self, **kwargs):
        if self. execute_everyday:
            self.execute_sunday    = True
            self.execute_monday    = True
            self.execute_tuesday   = True
            self.execute_wednesday = True
            self.execute_thursday  = True
            self.execute_friday    = True
            self.execute_saturday  = True
            
        super(Aggregation, self).save(**kwargs)
        
        
        #Execute now if the flag is set to do so.
        if self.execute_now:
            #Process aggregation
            pipeline = json.loads(self.pipeline)
            output_dict = {"$out": self.output_collection_name}
            pipeline.append(output_dict)
            result  = run_aggregation_pipeline(self.database_name, self.collection_name, pipeline)

@python_2_unicode_compatible
class SavedSearch(models.Model):

    user            = models.ForeignKey(settings.AUTH_USER_MODEL)
    group           = models.ForeignKey(Group, blank=True, null=True)
    output_format   = models.CharField(max_length=4, choices=OUTPUT_CHOICES,
                                        default="json")
    slug            = models.SlugField(max_length=100, unique=True)
    query           = models.TextField(max_length=2048, default="{}",            
                                        verbose_name="JSON Query")
    type_mapper     = models.TextField(max_length=2048, default="{}",            
                                        verbose_name="Map non-string variables to numbers or boolean")
    is_public       = models.BooleanField(default=False, blank=True,
                            help_text = "If checked, the search can be run without authentication")
    
    sort            = models.TextField(max_length=2048, default="", blank=True,
                                        verbose_name="Sort Dict",
                                        help_text="""e.g. [["somefield", 1], ["someotherfield", -1] ]""")
    
    return_keys     = models.TextField(max_length=2048, default="", blank=True,
                                      
                            help_text = """Default is blank which returns all keys.
                            Seperate keys by whitespace to limit the keys that are returned."""
                                        )
    
    default_limit   = models.IntegerField(default=getattr(settings, 'MONGO_LIMIT', 200),
                            help_text = "Limit results to this number unless specified otherwise.",
                                        )
    database_name   = models.CharField(max_length=100)
    collection_name = models.CharField(max_length=100)
    creation_date   = models.DateField(auto_now_add=True)
    
    class Meta:
        get_latest_by = "creation_date"
        ordering = ('-creation_date',)
        verbose_name_plural = "Saved Searches"

    def __str__(self):
        return "%s" % (self.slug)
        
        
@python_2_unicode_compatible        
class DatabaseAccessControl(models.Model):

    database_name   = models.CharField(max_length=256)
    collection_name = models.CharField(max_length=256)
    is_public       = models.BooleanField(default=False, blank=True)
    search_keys     =  models.TextField(max_length=4096, default="", blank=True,              
                        help_text = """The default, blank, returns all keys.
                                        Providing a list of keys, seperated by whitespace,
                                        limits the API search to only these keys.""")
    groups          = models.ManyToManyField(Group,  blank=True,
                                related_name = "djmongo_database_access_control")
    
    class Meta:
        #get_latest_by = "creation_date"
        #ordering = ('-creation_date',)
        verbose_name_plural = "Database Access Controls"
        unique_together =  (('database_name', 'collection_name'), )

    def __str__(self):
        return "%s/%s" % (self.database_name, self.collection_name )
        

