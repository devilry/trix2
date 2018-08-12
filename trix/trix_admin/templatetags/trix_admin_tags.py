from django import template

from trix.trix_admin.views.statistics import compute_stats_for_assignment


register = template.Library()


@register.simple_tag
def compute_and_set_stats_for_assignment(assignment, howsolved_filter, user_count,
                                         from_date=None, to_date=None):
    return compute_stats_for_assignment(assignment, howsolved_filter, user_count,
                                        from_date, to_date)


@register.filter
def cut_tag_preserve(tags, tag):
    """
    Cuts a tag from a list of tags without altering the original.
    """
    tag_list = tags[:]
    tag_list.remove(tag)
    return ",".join(tag_list)


@register.simple_tag
def order_in_use(order, order_list):
    if order in order_list and '-' + order not in order_list:
        return True
    return False


@register.filter
def reverse_sort(order, is_negative):
    return '-' + order if is_negative else order
