from django import template
from django.contrib.auth import get_user_model

register = template.Library()


@register.filter
def compute_stats(assignment, howsolved_filter):
    user_count = get_user_model().objects.all().count()
    if user_count == 0:
        return 0
    percentage = 0
    numerator = 0

    if howsolved_filter == 'bymyself':
        numerator = assignment.howsolved_set.\
            filter(howsolved='bymyself').count()
    elif howsolved_filter == 'withhelp':
        numerator = assignment.howsolved_set.\
            filter(howsolved='withhelp').count()
    else:  # Not solved
        bymyself_count = assignment.howsolved_set.\
            filter(howsolved='bymyself').count()
        withhelp_count = assignment.howsolved_set.\
            filter(howsolved='withhelp').count()
        numerator = user_count - (bymyself_count + withhelp_count)

    percentage = int(numerator / float(user_count) * 100)
    return percentage
