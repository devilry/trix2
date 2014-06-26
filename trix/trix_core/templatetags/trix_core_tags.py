from django import template

from trix.trix_core import trix_markdown

register = template.Library()


@register.simple_tag
def trix_assignment_markdown(inputmarkdown):
    r"""
    Tag to render the trix assignment text/solution markdown dialect.

    Example::

        {% load trix_core_tags %}
        {% trix_assignment_markdown "Hello world" %}
    """
    return trix_markdown.assignment_markdown(inputmarkdown)
