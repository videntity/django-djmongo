from django.db import models
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse


class HTTPAuthDeleteAPI(models.Model):

    database_name = models.CharField(max_length=256)
    collection_name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=100,
                            help_text="Give your API a unique name")
    search_keys = models.TextField(max_length=4096, default="", blank=True,
                                   help_text="""The default, blank, returns
                                                all keys. Providing a list of
                                                keys, separated by whitespace,
                                                limits the API search to only
                                                these keys.""")
    groups = models.ManyToManyField(
        Group, blank=True, related_name="djmongo_http_auth_delete_api")
    readme_md = models.TextField(max_length=4096, default="", blank=True)
    creation_date = models.DateField(auto_now_add=True)

    class Meta:
        # get_latest_by = "creation_date"
        # ordering = ('-creation_date',)
        unique_together = (('database_name', 'collection_name', 'slug'), )

    def __str__(self):
        return "%s/%s" % (self.database_name, self.collection_name)

    def url(self):
        return reverse('djmongo_api_httpauth_delete',
                       args=(self.database_name, self.collection_name, self.slug))

    def http_methods(self):
        return ['DELETE', 'GET', ]

    def auth_method(self):
        return 'httpauth'


class PublicDeleteAPI(models.Model):

    database_name = models.CharField(max_length=256)
    collection_name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=100,
                            help_text="Give your API a unique name")
    search_keys = models.TextField(max_length=4096, default="", blank=True,
                                   help_text="""The default, blank, returns
                                                all keys. Providing a list of
                                                keys, separated by whitespace,
                                                limits the API search to only
                                                these keys.""")
    readme_md = models.TextField(max_length=4096, default="", blank=True)
    creation_date = models.DateField(auto_now_add=True)

    class Meta:
        # get_latest_by = "creation_date"
        # ordering = ('-creation_date',)
        unique_together = (('database_name', 'collection_name', 'slug'), )

    def __str__(self):
        return "%s/%s/%s" % (self.database_name, self.collection_name, self.slug)

    def url(self):
        return reverse('djmongo_api_public_delete',
                       args=(self.database_name, self.collection_name, self.slug))

    def http_methods(self):
        return ['DELETE', 'GET', ]

    def auth_method(self):
        return 'public'


class IPAuthDeleteAPI(models.Model):

    database_name = models.CharField(max_length=256)
    collection_name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=100,
                            help_text="Give your API a unique name")
    from_ip = models.TextField(max_length=2048, default="127.0.0.1",
                               verbose_name=_("From IPs"),
                               help_text=_("Only accept requests from a IP in "
                                           "this list separated by whitespace "
                                           ". 0.0.0.0 means all."))
    search_keys = models.TextField(max_length=4096, default="", blank=True,
                                   help_text="""The default, blank, returns
                                                all keys. Providing a list of
                                                keys, separated by whitespace,
                                                limits the API search to only
                                                these keys.""")
    readme_md = models.TextField(max_length=4096, default="", blank=True)
    creation_date = models.DateField(auto_now_add=True)

    class Meta:
        # get_latest_by = "creation_date"
        # ordering = ('-creation_date',)
        unique_together = (('database_name', 'collection_name', 'slug'), )

    def allowable_ips(self):
        allowable_ips = self.from_ip.split(" ")
        return allowable_ips

    def __str__(self):
        return "%s/%s/%s" % (self.database_name, self.collection_name, self.slug)

    def url(self):
        return reverse('djmongo_api_ipauth_delete',
                       args=(self.database_name, self.collection_name, self.slug, 'json'))

    def http_methods(self):
        return ['DELETE', 'GET', ]

    def auth_method(self):
        return 'ipauth'


class OAuth2DeleteAPI(models.Model):

    database_name = models.CharField(max_length=256)
    collection_name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=100,
                            help_text="Give your API a unique name")
    scopes = models.CharField(max_length=1024, default="*", blank=True,
                              help_text="Space delimited list of scopes required. * means no scope is required.")
    search_keys = models.TextField(max_length=4096, default="", blank=True,
                                   help_text="""The default, blank, returns
                                                all keys. Providing a list of
                                                keys, separated by whitespace,
                                                limits the API search to only
                                                these keys.""")
    readme_md = models.TextField(max_length=4096, default="", blank=True)
    creation_date = models.DateField(auto_now_add=True)

    class Meta:
        # get_latest_by = "creation_date"
        # ordering = ('-creation_date',)
        unique_together = (('database_name', 'collection_name', 'slug'), )

    def __str__(self):
        return "%s/%s/%s" % (self.database_name, self.collection_name, self.slug)

    def url(self):
        return reverse('djmongo_api_oauth2_delete',
                       args=(self.database_name, self.collection_name, self.slug))

    def http_methods(self):
        return ['DELETE', 'GET']

    def auth_method(self):
        return 'oauth2'
