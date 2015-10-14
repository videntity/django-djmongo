import urllib, time, urlparse, random, string, uuid, re
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.core.mail import send_mail, mail_admins
from localflavor.us.us_states import US_STATES
from django.utils.translation import ugettext_lazy as _
from localflavor.us.models import PhoneNumberField, USPostalCodeField
import datetime
PERMISSION_CHOICES=( ('db-all',   'All MongoDB'),
                     ('db-write',  'Write MongoDB'),
                     ('db-read',   'Read MongoDB'),
                     ('create-other-users',  'create-other-users'),   
                     ('create-any-socialgraph', 'create-any-socialgraph'),
                     ('delete-any-socialgraph',  'delete-any-socialgraph'),
                    )


class Permission(models.Model):
    user  = models.ForeignKey(settings.AUTH_USER_MODEL)
    permission_name = models.CharField(max_length=50,
                choices=PERMISSION_CHOICES)

    def __unicode__(self):
        return '%s has the %s permission.' % (self.user.email, self.permission_name)

    class Meta:
        unique_together = (("user", "permission_name"),)



class SocialGraph(models.Model):
    
    grantor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="grantor")
    grantee = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="grantee")
    created_on  =  models.DateField(default=datetime.date.today)
   
    def __unicode__(self):
        return "%s --> %s since %s" % (self.grantor.username,
                                                self.grantee.username,
                                                self.created_on)
   
    class Meta:
        unique_together = (("grantor", "grantee"),)
        ordering = ('-created_on',)
        get_latest_by = "created_on"
