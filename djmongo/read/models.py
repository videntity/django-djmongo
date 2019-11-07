from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

OUTPUT_CHOICES = (("json", "JSON"),
                  ("html", "HTML"),
                  ("csv", "Comma Separated Value (.csv)"))


@python_2_unicode_compatible
class CustomOAuth2ReadAPI(models.Model):
    output_format = models.CharField(max_length=4,
                                     choices=OUTPUT_CHOICES,
                                     default="json")
    slug = models.SlugField(max_length=100,
                            help_text="Give your API a unique name")

    scopes = models.CharField(max_length=1024, default="*", blank=True,
                              help_text="Space delimited list of scopes required. * means no scope is required.")
    query = models.TextField(max_length=2048, default="{}",
                             verbose_name="JSON Query")
    type_mapper = models.TextField(
        max_length=2048,
        default="{}",
        verbose_name=_("Map non-string variables to numbers or Boolean"))
    sort = models.TextField(
        max_length=2048,
        default="",
        blank=True,
        verbose_name="Sort Dict",
        help_text="""e.g. [["somefield", 1], ["someotherfield", -1] ]""")

    return_keys = models.TextField(max_length=2048, default="", blank=True,
                                   help_text=_("Default is blank which "
                                               "returns all keys. Separate "
                                               "keys by white space to limit"
                                               "the keys that are returned."))

    default_limit = models.IntegerField(
        default=getattr(
            settings,
            'MONGO_LIMIT',
            200),
        help_text="Limit results to this number unless specified otherwise.",
    )
    database_name = models.CharField(max_length=100)
    collection_name = models.CharField(max_length=100)
    creation_date = models.DateField(auto_now_add=True)
    readme_md = models.TextField(max_length=4096, default="", blank=True)

    class Meta:
        get_latest_by = "creation_date"
        ordering = ('-creation_date',)
        unique_together = (('database_name', 'collection_name', 'slug'), )

    def __str__(self):
        return "%s/%s/%s" % (self.database_name, self.collection_name, self.slug)

    def auth_method(self):
        return 'oauth2'

    def http_methods(self):
        return ['GET', ]

    def url(self):
        return ""


@python_2_unicode_compatible
class CustomHTTPAuthReadAPI(models.Model):

    group = models.ForeignKey(
        Group, blank=True, null=True, on_delete=models.CASCADE)
    output_format = models.CharField(max_length=4,
                                     choices=OUTPUT_CHOICES,
                                     default="json")
    slug = models.SlugField(max_length=100,
                            help_text="Give your API a unique name")
    query = models.TextField(max_length=2048, default="{}",
                             verbose_name="JSON Query")
    type_mapper = models.TextField(
        max_length=2048,
        default="{}",
        verbose_name=_("Map non-string variables to numbers or Boolean"))
    sort = models.TextField(
        max_length=2048,
        default="",
        blank=True,
        verbose_name="Sort Dict",
        help_text="""e.g. [["somefield", 1], ["someotherfield", -1] ]""")

    return_keys = models.TextField(max_length=2048, default="", blank=True,
                                   help_text=_("Default is blank which "
                                               "returns all keys. Separate "
                                               "keys by white space to limit"
                                               "the keys that are returned."))

    default_limit = models.IntegerField(
        default=getattr(
            settings,
            'MONGO_LIMIT',
            200),
        help_text="Limit results to this number unless specified otherwise.",
    )
    database_name = models.CharField(max_length=100)
    collection_name = models.CharField(max_length=100)
    creation_date = models.DateField(auto_now_add=True)
    readme_md = models.TextField(max_length=4096, default="", blank=True)

    class Meta:
        get_latest_by = "creation_date"
        ordering = ('-creation_date',)

    def __str__(self):
        return "%s" % (self.slug)

    def url(self):
        return reverse('djmongo_run_custom_httpauth_read_api_by_slug', args=(self.slug,))

    def auth_method(self):
        return 'httpauth'

    def http_methods(self):
        return ['GET', ]


@python_2_unicode_compatible
class CustomIPAuthReadAPI(models.Model):

    output_format = models.CharField(max_length=4,
                                     choices=OUTPUT_CHOICES,
                                     default="json")
    slug = models.SlugField(max_length=100,
                            help_text="Give your API a unique name")
    query = models.TextField(max_length=2048, default="{}",
                             verbose_name="JSON Query")
    type_mapper = models.TextField(
        max_length=2048,
        default="{}",
        verbose_name=_("Map non-string variables to numbers or Boolean"))
    sort = models.TextField(
        max_length=2048,
        default="",
        blank=True,
        verbose_name="Sort Dict",
        help_text="""e.g. [["somefield", 1], ["someotherfield", -1] ]""")

    return_keys = models.TextField(max_length=2048, default="", blank=True,
                                   help_text=_("Default is blank which "
                                               "returns all keys. Separate "
                                               "keys by white space to limit"
                                               "the keys that are returned."))
    default_limit = models.IntegerField(
        default=getattr(
            settings,
            'MONGO_LIMIT',
            200),
        help_text="Limit results to this number unless specified otherwise.",
    )
    from_ip = models.TextField(max_length=2048, default="127.0.0.1",
                               verbose_name=_("From IPs"),
                               help_text=_("Only accept requests from a IP in "
                                           "this list separated by whitespace "
                                           ". 0.0.0.0 means all."))
    database_name = models.CharField(max_length=100)
    collection_name = models.CharField(max_length=100)
    readme_md = models.TextField(max_length=4096, default="", blank=True)
    creation_date = models.DateField(auto_now_add=True)

    class Meta:
        get_latest_by = "creation_date"
        ordering = ('-creation_date',)

    def allowable_ips(self):
        allowable_ips = self.from_ip.split(" ")
        return allowable_ips

    def __str__(self):
        return "%s" % (self.slug)

    def url(self):
        return reverse('djmongo_run_custom_ipauth_read_api_by_slug', args=(self.slug,))

    def http_methods(self):
        return ['GET', ]

    def auth_method(self):
        return 'ipauth'


@python_2_unicode_compatible
class CustomPublicReadAPI(models.Model):

    output_format = models.CharField(max_length=4,
                                     choices=OUTPUT_CHOICES,
                                     default="json")
    slug = models.SlugField(max_length=100,
                            help_text="Give your API a unique name")
    query = models.TextField(max_length=2048, default="{}",
                             verbose_name="JSON Query")
    type_mapper = models.TextField(
        max_length=2048,
        default="{}",
        verbose_name=_("Map non-string variables to numbers or Boolean"))
    sort = models.TextField(
        max_length=2048,
        default="",
        blank=True,
        verbose_name="Sort Dict",
        help_text="""e.g. [["somefield", 1], ["someotherfield", -1] ]""")

    return_keys = models.TextField(max_length=2048, default="", blank=True,
                                   help_text=_("Default is blank which "
                                               "returns all keys. Separate "
                                               "keys by white space to limit"
                                               "the keys that are returned."))
    default_limit = models.IntegerField(
        default=getattr(
            settings,
            'MONGO_LIMIT',
            200),
        help_text="Limit results to this number unless specified otherwise.",
    )
    database_name = models.CharField(max_length=100)
    collection_name = models.CharField(max_length=100)
    readme_md = models.TextField(max_length=4096, default="", blank=True)
    creation_date = models.DateField(auto_now_add=True)

    class Meta:
        get_latest_by = "creation_date"
        ordering = ('-creation_date',)

    def __str__(self):
        return "%s" % (self.slug)

    def url(self):
        return reverse('djmongo_run_custom_public_read_api_by_slug', args=(self.slug,))

    def http_methods(self):
        return ['GET', ]

    def auth_method(self):
        return 'public'


@python_2_unicode_compatible
class HTTPAuthReadAPI(models.Model):

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
        Group, blank=True, related_name="djmongo_http_auth_read_api")
    readme_md = models.TextField(max_length=4096, default="", blank=True)
    creation_date = models.DateField(auto_now_add=True)

    class Meta:
        # get_latest_by = "creation_date"
        # ordering = ('-creation_date',)
        unique_together = (('database_name', 'collection_name', 'slug'), )

    def __str__(self):
        return "%s/%s" % (self.database_name, self.collection_name)

    def url(self):
        return reverse('djmongo_api_httpauth_simple_search',
                       args=(self.database_name, self.collection_name, self.slug, 'json'))

    def json_url(self):
        return reverse('djmongo_api_httpauth_simple_search',
                       args=(self.database_name, self.collection_name, self.slug, 'json'))

    def csv_url(self):
        return reverse('djmongo_api_httpauth_simple_search',
                       args=(self.database_name, self.collection_name, self.slug, 'csv'))

    def html_url(self):
        return reverse('djmongo_api_httpauth_simple_search',
                       args=(self.database_name, self.collection_name, self.slug, 'html'))

    def http_methods(self):
        return ['GET', ]

    def auth_method(self):
        return 'httpauth'


@python_2_unicode_compatible
class PublicReadAPI(models.Model):

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
        return reverse('djmongo_api_public_simple_search',
                       args=(self.database_name, self.collection_name, self.slug, 'json'))

    def json_url(self):
        return reverse('djmongo_api_public_simple_search',
                       args=(self.database_name, self.collection_name, self.slug, 'json'))

    def csv_url(self):
        return reverse('djmongo_api_public_simple_search',
                       args=(self.database_name, self.collection_name, self.slug, 'csv'))

    def html_url(self):
        return reverse('djmongo_api_public_simple_search',
                       args=(self.database_name, self.collection_name, self.slug, 'html'))

    def http_methods(self):
        return ['GET', ]

    def auth_method(self):
        return 'public'


@python_2_unicode_compatible
class IPAuthReadAPI(models.Model):

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
        return reverse('djmongo_api_ipauth_simple_search',
                       args=(self.database_name, self.collection_name, self.slug, 'json'))

    def json_url(self):
        return reverse('djmongo_api_ipauth_simple_search',
                       args=(self.database_name, self.collection_name, self.slug, 'json'))

    def csv_url(self):
        return reverse('djmongo_api_ipauth_simple_search',
                       args=(self.database_name, self.collection_name, self.slug, 'csv'))

    def html_url(self):
        return reverse('djmongo_api_ipauth_simple_search',
                       args=(self.database_name, self.collection_name, self.slug, 'html'))

    def http_methods(self):
        return ['GET', ]

    def auth_method(self):
        return 'ipauth'


@python_2_unicode_compatible
class OAuth2ReadAPI(models.Model):

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
        return reverse('djmongo_api_oauth2_simple_search',
                       args=(self.database_name, self.collection_name, self.slug, 'json'))

    def json_url(self):
        return reverse('djmongo_api_oauth2_simple_search',
                       args=(self.database_name, self.collection_name, self.slug, 'json'))

    def csv_url(self):
        return reverse('djmongo_api_oauth2_simple_search',
                       args=(self.database_name, self.collection_name, self.slug, 'csv'))

    def html_url(self):
        return reverse('djmongo_api_oauth2_simple_search',
                       args=(self.database_name, self.collection_name, self.slug, 'html'))

    def http_methods(self):
        return ['GET', ]

    def auth_method(self):
        return 'oauth2'
