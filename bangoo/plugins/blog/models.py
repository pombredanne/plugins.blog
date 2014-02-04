from django.db import models
from hvad.models import TranslatableModel, TranslatedFields
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
from bangoo.content.models import Author
from django.utils.translation import ugettext_lazy as _


class ActiveManager(models.Manager):
    def get_query_set(self):
        return super(ActiveManager, self).get_query_set().filter(status = 2, published__isnull=False)


class Post(TranslatableModel):
    """Post model."""
    STATUS_CHOICES = (
        (1, _('Draft')),
        (2, _('Public')),
    )
    authors = models.ManyToManyField(Author, verbose_name=_('Authors'))
    status = models.IntegerField(verbose_name=_('Status'), choices=STATUS_CHOICES, default=1)
    allow_comments = models.BooleanField(verbose_name=_('Allow comments'), default=True)
    created = models.DateTimeField(verbose_name=_('created'), auto_now_add=True)
    published = models.DateTimeField(verbose_name=_('Published'), blank=True, null=True)
    last_modified = models.DateTimeField(verbose_name=_('Last modified'), auto_now=True)
    tags = TaggableManager(through='TaggedPost')
    translations = TranslatedFields(
        slug = models.CharField(verbose_name=_('slug'), max_length=255, unique_for_date="created"),
        title = models.CharField(verbose_name=_('title'), max_length=255),
        intro = models.TextField(verbose_name=_('intro'), blank=True, null=True),
        text = models.TextField(verbose_name=_('content'), blank=True, null=True),
        meta = {
            'permissions': (
                    ('Can list all posts', 'list_posts'),
                )
        }
    )
    actives = ActiveManager()

    @property
    def local_tags(self):
        if self.language_code:
            return self.tags.filter(blog_taggedpost_items__language_code=self.language_code)
        return self.tags.all()


class TaggedPost(TaggedItemBase):
    content_object = models.ForeignKey('Post')
    language_code = models.CharField(max_length=2, blank=True, null=True)