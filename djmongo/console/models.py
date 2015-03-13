from django.db import models

from django.template.defaultfilters import slugify



OUTPUT_CHOICES = (("csv","Comma Seperated Value (.csv)"),
                  ("xls","Microsoft Excel(xls)"),
                  ("json","JSON"),
                  ("xml","XML"))

class CreateHistory(models.Model):

    database_name   = models.CharField(max_length=100, unique=True)
    collection_name = models.CharField(max_length=100, unique=True)
    history         = models.BooleanField(default=False,
                            help_text= "Check this to create a historical collection. When items are updated the old data is saved in another collection")
    
    class Meta:
        #get_latest_by = "creation_date"
        #ordering = ('-creation_date',)
        verbose_name_plural = "Saved Searches"

    def __unicode__(self):
        return "%s/%s" % (self.database_name, self.collection_name )
        

