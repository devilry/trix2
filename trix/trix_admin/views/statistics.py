from django.views.generic import ListView
from django.views.generic import View
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django_cradmin import crapp
from django_cradmin.viewhelpers import objecttable

from trix.trix_core import models as trix_models
import csv
import codecs
import cStringIO
from trix.trix_core.models import HowSolved


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
        return 0

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

    percentage = numerator / float(user_count) * 100
    return percentage


def get_usercount_within_course(course_tag_id):
    user_ids_within_course = HowSolved.objects\
        .filter(assignment__tags=course_tag_id)\
        .values_list('user_id', flat=True)
    user_count = get_user_model().objects\
        .filter(id__in=user_ids_within_course)\
        .distinct()\
        .count()
    return user_count


class AssignmentStatsCsv(View):

    def get(self, request, *args, **kwargs):
        course_tag_id = request.GET.get('tag', None)
        if not course_tag_id:
            return HttpResponseBadRequest()
        queryset = trix_models.Assignment.objects.filter(tags__id=course_tag_id)

        user_count = get_usercount_within_course(course_tag_id)
        response = HttpResponse(content_type='text/csv')
        try:
            response['Content-Disposition'] = 'attachment; filename="trix-statistics.csv"'
            csvwriter = UnicodeWriter(response)  # csv.writer(response, dialect='excel')
            csvwriter.writerow([_('Simple statitics showing percentage share of how the assignments where solved')])
            csvwriter.writerow([_('Total number of users'), str(user_count)])
            csvwriter.writerow('')
            csvwriter.writerow([_('Assignment title'), _('Percentage')])
            for assignment in queryset:
                csvwriter.writerow([assignment.title])
                csvwriter.writerow([
                    _('Completed by their own'),
                    "{} %".format(compute_stats_for_assignment(assignment, 'bymyself', user_count))])
                csvwriter.writerow([
                    _('Completed with help'),
                    "{} %".format(compute_stats_for_assignment(assignment, 'withhelp', user_count))])
                csvwriter.writerow([_('Not completed'), "{} %".format(
                    compute_stats_for_assignment(assignment, 'notsolved', user_count))])
                csvwriter.writerow('')
        except Exception, e:
            raise e
        return response


class StatisticsChartView(ListView):
    """
    Class for the statistics charts displayed.

    This views takes the pk of a Tag to filter the assignments
    """
    template_name = 'trix_admin/statistics.django.html'
    model = trix_models.Assignment
    context_object_name = 'assignment_list'
    paginate_by = 20
    queryset = None

    def get(self, request, *args, **kwargs):
        self.tag_id = kwargs['pk']
        return super(StatisticsChartView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return super(StatisticsChartView, self).get_queryset()\
            .filter(tags__id=self.tag_id)

    def get_context_data(self, **kwargs):
        context = super(StatisticsChartView, self).get_context_data(**kwargs)
        context['user_count'] = get_usercount_within_course(self.request.cradmin_role.course_tag_id)
        context['assignment_count'] = self.get_queryset().count()
        context['tag_id'] = self.tag_id
        return context


class TitleColumn(objecttable.SingleActionColumn):
    modelfield = 'tag'

    def get_actionurl(self, obj):
        return self.reverse_appurl('view', args=[obj.id])


class StatisticsView(objecttable.ObjectTableView):
    model = trix_models.Tag
    columns = [
        TitleColumn,
    ]

    def get_queryset_for_role(self, course):
        return self.model.objects.all()


class App(crapp.App):
    appurls = [
        crapp.Url(r'^$', StatisticsView.as_view(), name=crapp.INDEXVIEW_NAME),
        crapp.Url(r'^view/(?P<pk>\d+)$', StatisticsChartView.as_view(), name='view'),
    ]
