from django.db import models
from django.contrib.auth.models import Group


class WriteAPI(models.Model):

    slug            = models.SlugField(max_length=100, unique=True)
    database_name   = models.CharField(max_length=100)
    collection_name = models.CharField(max_length=100)
    json_schema           = models.TextField(max_length=2048, default="{}",            
                                        verbose_name="JSON Schema",
                                        help_text="""Default "{}", means no JSONschema.""")
    from_ip           = models.TextField(max_length=2048, default="", blank=True,           
                                        verbose_name="From IP",
                                        help_text="""Only accept requests from a IP in this list (separated by whitespace).""")
    

    creation_date   = models.DateField(auto_now_add=True)
    
    class Meta:
        get_latest_by = "creation_date"
        ordering = ('-creation_date',)
        verbose_name_plural = "Write APIs"

    def __unicode__(self):
        return "%s" % (self.slug)
      
        

