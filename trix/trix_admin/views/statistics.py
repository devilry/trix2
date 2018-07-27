from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.views.generic import ListView
from django.views.generic import View
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from cradmin_legacy import crapp
from cradmin_legacy.viewhelpers import objecttable
from django.utils.http import urlencode
from django.core.exceptions import FieldError

import csv
import codecs
import cStringIO
from trix.trix_core import models as trix_models


class UnicodeWriter:
    """

    Picked from https://docs.python.org/2/library/csv.html#examples

    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


def compute_stats_for_assignment(assignment, howsolved_filter, user_count):
    if user_count == 0:
        return {'percent': 0, 'count': 0}

    if howsolved_filter == 'bymyself':
        numerator = assignment.howsolved_set.filter(howsolved='bymyself').count()
    elif howsolved_filter == 'withhelp':
        numerator = assignment.howsolved_set.filter(howsolved='withhelp').count()
    else:  # Not solved
        bymyself_count = assignment.howsolved_set.filter(howsolved='bymyself').count()
        withhelp_count = assignment.howsolved_set.filter(howsolved='withhelp').count()
        numerator = user_count - (bymyself_count + withhelp_count)

    percentage = numerator / float(user_count) * 100
    return {'percent': percentage, 'count': numerator}


def get_usercount_within_assignments(assignments):
    user_ids = (trix_models.HowSolved.objects
                .filter(assignment__in=assignments)
                .values_list('user_id', flat=True))
    user_count = (get_user_model().objects
                  .filter(id__in=user_ids)
                  .distinct()
                  .count())
    return user_count


class AssignmentStatsMixin(object):
    def get_tags(self, course_tag=None):
        tags_string = self.request.GET.get('tags')
        if tags_string:
            tags = []
            removetags = []
            for tag in tags_string.split(','):
                tag = tag.strip()
                if tag:
                    if tag.startswith('-'):
                        removetags.append(tag.lstrip('-'))
                    else:
                        tags.append(tag)
            for removetag in removetags:
                tags.remove(removetag)
        else:
            tags = []
        if course_tag is not None and course_tag not in tags:
            tags.append(course_tag)
        return tags

    def get_sort_list(self):
        order_list = self.request.GET.get('ordering')
        if order_list:
            sort_list = []
            for order in order_list.split(','):
                order = order.strip()
                sort_list.append(order)
        else:
            sort_list = []
        return sort_list

    def get_queryset(self):
        queryset = super(AssignmentStatsMixin, self).get_queryset()
        for tagstring in self.tags:
            queryset = queryset.filter(tags__tag=tagstring)
        return queryset


class AssignmentStatsCsv(AssignmentStatsMixin, View):

    def get(self, request, *args, **kwargs):
        self.tags = self.get_tags()
        if not self.tags:
            return HttpResponseBadRequest()
        if self.request.cradmin_role.course_tag.tag not in self.tags:
            raise PermissionDenied()
        assignmentqueryset = self.get_queryset()

        user_count = get_usercount_within_assignments(assignmentqueryset)
        response = HttpResponse(content_type='text/csv')
        csv.register_dialect('semicolons', delimiter=';')

        try:
            response['Content-Disposition'] = 'attachment; filename="trix-statistics.csv"'
            csvwriter = UnicodeWriter(response, dialect='semicolons', encoding="utf-8")
            csvwriter.writerow([_('Simple statistics showing percentage share of how the '
                                  'assignments where solved')])
            csvwriter.writerow([_('Total number of users'), str(user_count)])
            csvwriter.writerow('')
            csvwriter.writerow([_('Assignment title'), _('Percentage'), _('Number')])
            for assignment in assignmentqueryset:
                csvwriter.writerow([assignment.title])
                bymyself = compute_stats_for_assignment(assignment,
                                                        'bymyself',
                                                        user_count)
                csvwriter.writerow([
                    _('Completed by their own'),
                    "{}%".format(bymyself['percent']),
                    "{}".format(bymyself['count'])])
                withhelp = compute_stats_for_assignment(assignment,
                                                        'withhelp',
                                                        user_count)
                csvwriter.writerow([
                    _('Completed with help'),
                    "{}%".format(withhelp['percent']),
                    "{}".format(withhelp['count'])])
                notsolved = compute_stats_for_assignment(assignment, 'notsolved', user_count)
                csvwriter.writerow([_('Not completed'),
                                    "{}%".format(notsolved['percent']),
                                    "{}".format(notsolved['count'])])
                csvwriter.writerow('')
        except Exception, e:
            raise e
        return response


class StatisticsChartView(AssignmentStatsMixin, ListView):
    """
    Class for the statistics charts displayed.

    This views takes the pk of a Tag to filter the assignments
    """
    template_name = 'trix_admin/statistics.django.html'
    model = trix_models.Assignment
    context_object_name = 'assignment_list'
    paginate_by = 20

    def get(self, request, *args, **kwargs):
        self.tags = self.get_tags(self.request.cradmin_role.course_tag.tag)
        self.sort_list = self.get_sort_list()
        return super(StatisticsChartView, self).get(request, *args, **kwargs)

    def _get_selectable_tags(self):
        tags = (trix_models.Tag.objects
                .filter(assignment__in=self.get_queryset())
                .exclude(tag__in=self.tags)
                .order_by('tag')
                .distinct()
                .values_list('tag', flat=True))
        return tags

    def get_context_data(self, **kwargs):
        context = super(StatisticsChartView, self).get_context_data(**kwargs)
        context['user_count'] = get_usercount_within_assignments(self.get_queryset())
        context['assignment_count'] = self.get_queryset().count()
        context['selected_tags_string'] = ','.join(self.tags)
        context['selected_tags_list'] = self.tags
        context['selectable_tags_list'] = self._get_selectable_tags()
        context['course_tag'] = self.request.cradmin_role.course_tag.tag
        context['sort_list'] = ','.join(self.sort_list)
        context['selectable_sort_list'] = [(_('Title'), 'title'),
                                           (_('Date created'), 'created_datetime'),
                                           (_('Last updated'), 'lastupdate_datetime')]
        return context

    def get_ordering(self):
        ordering = self.request.GET.get('ordering', None)
        if ordering is not None:
            ordering = ordering.split(',')
            for order in ordering:
                try:
                    str(self.model.objects.order_by(order))
                except FieldError:
                    return None
        return ordering


class TagColumn(objecttable.SingleActionColumn):
    modelfield = 'tag'

    def get_actionurl(self, tag):
        tags_string = u'{},{}'.format(self.view.request.cradmin_role.course_tag.tag, tag.tag)
        return '{}?{}'.format(self.reverse_appurl(''), urlencode({
            'tags': tags_string
        }))


class AssignmentCountColumn(objecttable.PlainTextColumn):
    orderingfield = 'assignment__count'

    def get_header(self):
        return _('Number of assignments')

    def render_value(self, tag):
        return tag.assignment__count


class StatisticsView(objecttable.ObjectTableView):
    model = trix_models.Tag
    columns = [
        TagColumn,
        AssignmentCountColumn,
    ]
    searchfields = [
        'tag'
    ]

    def get_queryset_for_role(self, course):
        return self.model.objects\
            .annotate(Count('assignment', distinct=True))\
            .exclude(tag=course.course_tag.tag)


class App(crapp.App):
    appurls = [
        crapp.Url(r'^$', StatisticsChartView.as_view(), name=crapp.INDEXVIEW_NAME),
        crapp.Url(r'^ascsv$', AssignmentStatsCsv.as_view(), name='ascsv'),
    ]
