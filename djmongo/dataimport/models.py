from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import os, uuid, json
from django.template.defaultfilters import slugify
from .utils import bulk_csv_import_mongo
from django.utils.encoding import python_2_unicode_compatible

def update_import_filename(instance, filename):
    path = "imports/"
    format = instance.user.username + "-" + str(uuid.uuid4())[0:5] + "-" +filename
    return os.path.join(path, format)


INPUT_CHOICES = (("csv","Comma Seperated Value (.csv)"),
                )
@python_2_unicode_compatible
class DataImport(models.Model):

    user            = models.ForeignKey(settings.AUTH_USER_MODEL)
    file1            = models.FileField(upload_to=update_import_filename,
                                        verbose_name = "File to be imported")
    input_format    = models.CharField(max_length=4, choices=INPUT_CHOICES,
                                        default="csv")
    
    delete_collection_before_import   = models.BooleanField(default=False)

    status         = models.CharField(max_length=10, default="New",
                                        verbose_name="Status", editable = False)
    
    response        = models.TextField(max_length=2048, default="", blank=True,
                                        verbose_name="Response")
    
    database_name   = models.CharField(max_length=256)

    collection_name = models.CharField(max_length=256)
    
    creation_date     = models.DateField(auto_now_add=True)
    
    class Meta:
        get_latest_by = "creation_date"
        ordering = ('-creation_date',)

    def __str__(self):
        return "%s by %s %s" % (self.title, self.user.first_name,
                                self.user.last_name)
    def save(self, **kwargs):
        self.status = "Proccessing"
        
        #Generate the slug if the record it was not already defined.
        super(DataImport, self).save(**kwargs)
        #process the file
        result = bulk_csv_import_mongo(self.file1,
                                       self.database_name,
                                       self.collection_name,
                                       self.delete_collection_before_import) 
        
        #report results
        self.response = json.dumps(result, indent = 4)
        self.status = "Complete"
        #re-write db after complete
        super(DataImport, self).save(**kwargs)
        

    
    
    
