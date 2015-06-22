# coding: utf-8

from django import template

register = template.Library()


@register.simple_tag
def include_css(post):
    assets = []

    for asset in post.asset_set.filter(mime_type__in=['text/css']):
        assets.append('<link href="{0}" rel="stylesheet" type="text/css">'.format(asset.file.url))

    return '\n'.join(assets)


@register.simple_tag
def include_scripts(post):
    assets = []

    for asset in post.asset_set.filter(mime_type__in=['application/javascript', 'text/javascript']):
        assets.append('<script src="{0}" type="{1}"></script>'.format(asset.file.url, asset.mime_type))

    return '\n'.join(assets)


@register.simple_tag
def include_cover(post, name):
    asset = post.asset_set.filter(file__endswith=name).first()
    if asset:
        return '<img src="{0}">'.format(asset.file.url)
