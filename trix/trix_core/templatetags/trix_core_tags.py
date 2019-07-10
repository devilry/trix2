from django import template

from trix.trix_core import trix_markdown

register = template.Library()


@register.simple_tag
def trix_assignment_markdown(inputmarkdown):
    """
    Tag to render the trix assignment text/solution markdown dialect.

    Example::

        {% load trix_core_tags %}
        {% trix_assignment_markdown "Hello world" %}
    """
    return trix_markdown.assignment_markdown(inputmarkdown)


@register.simple_tag(takes_context=True)
def url_replace(context, field, value):
    dict_ = context['request'].GET.copy()
    if value == '' or value is None:
        try:
            del dict_[field]
        except KeyError:
            pass
    else:
        dict_[field] = value
    return dict_.urlencode()


@register.filter
def add_string_list(string_list, item):
    return string_list + ',' + item


@register.filter
def startswith(tag, item):
    return tag.startswith(item)
