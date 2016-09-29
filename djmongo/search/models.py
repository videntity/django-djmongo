from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

OUTPUT_CHOICES = (("json", "JSON"),
                  ("html", "HTML"),
                  ("csv", "Comma Seperated Value (.csv)"))


@python_2_unicode_compatible
class SavedSearch(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    group = models.ForeignKey(Group, blank=True, null=True)
    output_format = models.CharField(max_length=4,
                                     choices=OUTPUT_CHOICES,
                                     default="json")
    slug = models.SlugField(max_length=100, unique=True)
    query = models.TextField(max_length=2048, default="{}",
                             verbose_name="JSON Query")
    type_mapper = models.TextField(
        max_length=2048,
        default="{}",
        verbose_name=_("Map non-string variables to numbers or Boolean"))
    is_public = models.BooleanField(
        default=False,
        blank=True,
        help_text=_("If checked, the search can "
                    "be run without authentication"))

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

    class Meta:
        get_latest_by = "creation_date"
        ordering = ('-creation_date',)
        verbose_name_plural = "Saved Searches"

    def __str__(self):
        return "%s" % (self.slug)

    def url(self):
        return reverse('run_saved_search_by_slug', args=(self.slug,))

@python_2_unicode_compatible
class DatabaseAccessControl(models.Model):

    database_name = models.CharField(max_length=256)
    collection_name = models.CharField(max_length=256)
    is_public = models.BooleanField(default=False, blank=True)
    search_keys = models.TextField(max_length=4096, default="", blank=True,
                                   help_text="""The default, blank, returns
                                                all keys. Providing a list of
                                                keys, separated by whitespace,
                                                limits the API search to only
                                                these keys.""")
    groups = models.ManyToManyField(
        Group, blank=True, related_name="djmongo_database_access_control")

    class Meta:
        # get_latest_by = "creation_date"
        # ordering = ('-creation_date',)
        verbose_name_plural = "Search APIs using HTTPAuth"
        verbose_name = "Search API using HTTPAuth"
        unique_together = (('database_name', 'collection_name'), )

    def __str__(self):
        return "%s/%s" % (self.database_name, self.collection_name)
    
    def json_url(self):
        return reverse('djmongo_api_public_search_json_w_params',
                       args=(self.database_name, self.collection_name))
    def csv_url(self):
        return reverse('djmongo_api_public_search_csv_w_params',
                       args=(self.database_name, self.collection_name))
    def html_url(self):
        return reverse('djmongo_api_public_search_html_w_params',
                       args=(self.database_name, self.collection_name))
    
@python_2_unicode_compatible
class PublicReadAPI(models.Model):

    database_name = models.CharField(max_length=256)
    collection_name = models.CharField(max_length=256)
    search_keys = models.TextField(max_length=4096, default="", blank=True,
                                   help_text="""The default, blank, returns
                                                all keys. Providing a list of
                                                keys, separated by whitespace,
                                                limits the API search to only
                                                these keys.""")
    class Meta:
        # get_latest_by = "creation_date"
        # ordering = ('-creation_date',)
        verbose_name_plural = "Search APIs using No Auth (Public)"
        verbose_name = "Search API using No Auth (Public)"
        unique_together = (('database_name', 'collection_name'), )

    def __str__(self):
        return "%s/%s" % (self.database_name, self.collection_name)
    
    def json_url(self):
        return reverse('djmongo_api_public_search_json_w_params',
                       args=(self.database_name, self.collection_name))
    def csv_url(self):
        return reverse('djmongo_api_public_search_csv_w_params',
                       args=(self.database_name, self.collection_name))
    def html_url(self):
        return reverse('djmongo_api_public_search_html_w_params',
                       args=(self.database_name, self.collection_name))
