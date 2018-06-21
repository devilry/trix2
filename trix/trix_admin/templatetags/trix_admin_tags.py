from django import template

from trix.trix_admin.views.statistics import compute_stats_for_assignment


register = template.Library()


@register.simple_tag
def compute_and_set_stats_for_assignment(assignment, howsolved_filter, user_count):
    return compute_stats_for_assignment(assignment, howsolved_filter, user_count)
