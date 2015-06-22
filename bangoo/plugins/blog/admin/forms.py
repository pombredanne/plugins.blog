# coding: utf-8

import mimetypes
import os
import zipfile

from datetime import datetime

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from ..models import Post, Asset


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'preview', 'tags')

    def __init__(self, post=None, files=None, **kwargs):
        if post:
            self.post_state = post.pop('state')[0]
        super(PostForm, self).__init__(post, files, **kwargs)
        self.fields['assets'] = forms.FileField(required=False, help_text=_('.zip archive required'), label=_('Upload assets'))

    def clean_assets(self):
        if self.cleaned_data['assets'] and not zipfile.is_zipfile(self.cleaned_data['assets']):
            raise ValidationError(_('Invalid file'))
        return self.cleaned_data['assets']

    def save(self, commit=True):
        with transaction.atomic():
            self.instance.slug = slugify(self.cleaned_data['title'])
            if self.post_state == 'publish':
                self.instance.published_at = datetime.now()
            elif self.post_state == 'draft':
                self.instance.published_at = None
            instance = super(PostForm, self).save(commit)

            if self.cleaned_data['assets']:
                out_root = os.path.join(settings.MEDIA_ROOT, 'blog', str(instance.pk))
                if os.path.exists(out_root):
                    for filename in os.listdir(out_root):
                        os.remove(os.path.join(out_root, filename))
                    Asset.objects.filter(post=self.instance).delete()

                archive = zipfile.ZipFile(self.cleaned_data['assets'])
                for filename in archive.namelist():
                    if len(filename.split('/')) == 1:
                        archive.extract(filename, path=out_root)
                        out = os.path.join('blog', str(instance.pk), filename)
                        Asset.objects.create(post=self.instance, file=out, mime_type=mimetypes.guess_type(out)[0])

            return instance


class PostPublishForm(forms.Form):
    state = forms.ChoiceField(
        choices=(
            ('publish', None),
            ('draft', None)
        )
    )

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance')
        super(PostPublishForm, self).__init__(*args, **kwargs)

    def save(self):
        if self.cleaned_data['state'] == 'publish':
            self.instance.published_at = datetime.now()
        else:
            self.instance.published_at = None
        self.instance.save()
        return self.instance