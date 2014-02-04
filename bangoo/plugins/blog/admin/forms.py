#encoding: utf8
from django import forms
from ..models import Post, TaggedPost
from crispy_forms.helper import FormHelper
from django.conf import settings
from crispy_forms.layout import Layout, Div, Submit
from crispy_forms.bootstrap import FormActions, Accordion, AccordionGroup, Panel
from django.utils.translation import ugettext_lazy as _
from taggit.models import Tag
from richforms.fields import TagItField
from content.models import Author
from richforms import widgets
from django.template.defaultfilters import slugify


class EditPostForm(forms.ModelForm):
    authors = forms.ModelMultipleChoiceField(queryset=Author.objects.filter(is_active=True), help_text='',
                                             widget=widgets.SelectMupltipleWithCheckbox(widget_attrs={'filter': "true", "width": "800"}) )

    class Meta:
        model = Post
        fields = ['authors', 'allow_comments']
    
    def __init__(self, *args, **kwargs):
        self.base_fields['authors'].help_text = ''
        super(EditPostForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout()
        a = Accordion()
        self.helper.layout.fields.append(a)
        for lang_code, lang in settings.LANGUAGES:
            required = True if lang_code == settings.LANGUAGE_CODE.split('-')[1] else False
            self.fields['title_%s' % lang_code] = forms.CharField(max_length=200, label='Title (%s)' % lang, required=required)
            self.fields['intro_%s' % lang_code] = forms.CharField(required=False, label='Introduction (%s)' % lang,
                                                                    widget=forms.Textarea)
            self.fields['text_%s' % lang_code] = forms.CharField(required=required, label='Content (%s)' % lang, 
                                                                    widget=forms.Textarea)
            self.fields['tags_%s' % lang_code] = TagItField(queryset=Tag.objects.all(), to_field_name='name',
                                                            required=False, label='Tags (%s)' % lang, allow_append=True)
            if self.instance.pk:
                try:
                    trans = self.instance.translations.get(language_code=lang_code)
                    self.fields['title_%s' % lang_code].initial = trans.title
                    self.fields['intro_%s' % lang_code].initial = trans.intro
                    self.fields['text_%s' % lang_code].initial = trans.text
                    self.fields['tags_%s' % lang_code].initial = \
                        self.instance.tags.filter(blog_taggedpost_items__language_code=lang_code)
                except:
                    pass
            ag = AccordionGroup( _('Text in %(language)s' % {'language': lang.lower()}), 
                                 'title_%s' % lang_code, 'intro_%s' % lang_code, 
                                 'text_%s' % lang_code, 'tags_%s' % lang_code )
            a.fields.append(ag)
        p = Panel(_('Post settings'), 'authors', 'allow_comments', css_id="post-settings")
        self.helper.layout.fields.append(p)
        self.helper.layout.append(FormActions(Submit('submit', u'Ment', css_class='btn-primary')))

    def clean(self, *args, **kwargs):
        data = super(EditPostForm, self).clean(*args, **kwargs)
        if not self.is_valid():
            return data
        data['post_texts'] = []
        for lang_code, lang in settings.LANGUAGES:
            title = data['title_%s' % lang_code]
            introduction = data['intro_%s' % lang_code]
            text = data['text_%s' % lang_code]
            if all([len(title), len(text)]):
                p = {'language_code': lang_code, 'title': title, 'intro': introduction, 'text': text, 
                     'slug': slugify(title), 'tags': data['tags_%s' % lang_code]}
                data['post_texts'].append(p)
        return data

    def save(self, *args, **kwargs):
        obj = super(EditPostForm, self).save(*args, **kwargs)
        obj.translations.all().delete()
        obj.tags.clear()
        for pt in self.cleaned_data['post_texts']:
            obj.translate(pt['language_code'])
            for label in pt.keys():
                if label == 'language_code':
                    continue
                setattr(obj, label, pt[label])
            obj.save()
            for tag in pt['tags']:
                _ = TaggedPost.objects.create(tag=tag, content_object=obj, language_code=pt['language_code'])
        return obj