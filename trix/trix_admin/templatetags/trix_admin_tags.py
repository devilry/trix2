from django import template
from django.contrib.auth import get_user_model

from trix.trix_core import models as trix_models

register = template.Library()

@register.filter
def compute_stats(assignment, howsolved_filter):
    user_count = get_user_model().objects.all().count()
    if user_count == 0:
        return 0
    percentage = 0
    numerator = 0

    if howsolved_filter == 'bymyself':
        numerator = assignment.howsolved_set.filter(howsolved='bymyself').count()
    elif howsolved_filter == 'withhelp':
        numerator = assignment.howsolved_set.filter(howsolved='withhelp').count()
    else: # Not solved
        numerator = 0

    percentage = int(numerator / float(user_count) * 100) 
    return percentage