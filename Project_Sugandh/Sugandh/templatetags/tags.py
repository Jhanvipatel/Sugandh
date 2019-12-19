from django import template
from django.template.defaultfilters import stringfilter
from django.template.exceptions import TemplateSyntaxError

register = template.Library()


@register.filter(name='parse_img_url')
@stringfilter
def parse_image_url(value):
    value = value.strip('["]\'')
    from random import choice
    x = choice(value.split(','))
    return x.strip("'] ").replace("&#39;]", '')


@register.filter(name='img_url_list')
@stringfilter
def parse_image_url(value):
    value = value.strip('["]\'')
    return [url.strip("'] ").replace("&#39;]", '') for url in value.split(',')]

@register.filter(name='urls')
@stringfilter
def urls(value):
    return value.strip('[]"').split(', ')

@register.filter(name='get_first')
def get_first(value):
    return value[0]

@register.filter(name='currency')
def currency(value):
    return '₹ ''{:,}'.format(int(value) if value else 0)


@register.simple_tag
def get_product_variant(product, size=None):
    if size is None:
        raise TemplateSyntaxError('size required for fetching product price')
    return product.variants.filter(size=size).first()


@register.simple_tag
def filter_queryset(queryset, **kwargs):
    return queryset.filter(**kwargs)
