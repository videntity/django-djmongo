from django.db import models
from django.contrib.auth.models import Group


class WriteAPIHTTPAuth(models.Model):

    slug            = models.SlugField(max_length=100, unique=True)
    database_name   = models.CharField(max_length=100)
    collection_name = models.CharField(max_length=100)
    json_schema     = models.TextField(max_length=2048, default="{}",            
                        verbose_name="JSON Schema",
                        help_text="""Default "{}", means no JSONschema.""")
    creation_date   = models.DateField(auto_now_add=True)
    
    class Meta:
        get_latest_by = "creation_date"
        ordering = ('-creation_date',)
        verbose_name_plural = "Write APIs with HTTPAuth Auth"
        verbose_name = "Write API with HTTPAuth Auth"

    def __unicode__(self):
        return "%s" % (self.slug)
      
        

class WriteAPIIP(models.Model):

    slug            = models.SlugField(max_length=100, unique=True)
    database_name   = models.CharField(max_length=100)
    collection_name = models.CharField(max_length=100)
    json_schema     = models.TextField(max_length=2048, default="{}",            
                        verbose_name="JSON Schema",
                        help_text="""Default "{}", means no JSONschema.""")
    from_ip          = models.TextField(max_length=2048, default="127.0.0.1",           
                            verbose_name="From IPs",
                            help_text="""Only accept requests from a IP in this list (separated by whitespace). 0.0.0.0 means all.""")
    creation_date   = models.DateField(auto_now_add=True)
    
    class Meta:
        get_latest_by = "creation_date"
        ordering = ('-creation_date',)
        verbose_name_plural = "Write APIs with IP address Auth"
        verbose_name = "Write API with IP address Auth"
        
    def allowable_ips(self):
        allowable_ips = self.from_ip.split(" ")
        return  allowable_ips

    def __unicode__(self):
        return "%s" % (self.slug)
      
class WriteAPIoAuth2(models.Model):

    slug            = models.SlugField(max_length=100, unique=True)
    database_name   = models.CharField(max_length=100)
    collection_name = models.CharField(max_length=100)
    json_schema     = models.TextField(max_length=2048, default="{}",            
                        verbose_name="JSON Schema",
                        help_text="""Default "{}", means no JSONschema.""")
    creation_date   = models.DateField(auto_now_add=True)
    
    class Meta:
        get_latest_by = "creation_date"
        ordering = ('-creation_date',)
        verbose_name_plural = "Write APIs with oAuth2 Auth"
        verbose_name        = "Write API with oAuth2 Auth"

    def __unicode__(self):
        return "%s" % (self.slug)
      


