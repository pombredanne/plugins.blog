# coding: utf-8
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from taggit.managers import TaggableManager


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('author'))

    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    content = models.TextField()
    preview = models.TextField(blank=True, null=True, help_text=_('This short preview text is shown instead of the '
                                                                  'full article if it is given.'))

    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True)
    tags = TaggableManager(blank=True)

    class Meta:
        ordering = ['-created_at']


class Asset(models.Model):
    post = models.ForeignKey(Post)
    file = models.FileField()
    mime_type = models.CharField(max_length=32)
