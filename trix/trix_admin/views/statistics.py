from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.views.generic import ListView
from django.views.generic import View
from django.utils.translation import gettext as _
from cradmin_legacy import crapp

import csv
from trix.trix_core import models as trix_models


def compute_stats_for_assignment(assignment, howsolved_filter, user_count,
                                 from_date=None, to_date=None):
    if user_count == 0:
        return {'percent': 0, 'count': 0}

    if howsolved_filter != 'notsolved':
        queryset = assignment.howsolved_set.filter(howsolved=howsolved_filter)
    else:
        queryset = assignment.howsolved_set.filter(Q(howsolved='bymyself')
                                                   | Q(howsolved='withhelp'))  # noqa: W503

    # Filter based on date if present
    queryset = queryset.filter(solved_datetime__date__gte=from_date) if from_date else queryset
    queryset = queryset.filter(solved_datetime__date__lte=to_date) if to_date else queryset
    count = queryset.count()
    # Not solved is number of users that has solved something, but not this task
    numerator = user_count - count if howsolved_filter == 'notsolved' else count
    percentage = numerator / float(user_count) * 100
    return {'percent': percentage, 'count': numerator}


def get_usercount_within_assignments(assignments, from_date=None, to_date=None):
    user_ids = trix_models.HowSolved.objects.filter(assignment__in=assignments)
    user_ids = user_ids.filter(solved_datetime__date__gte=from_date) if from_date else user_ids
    user_ids = user_ids.filter(solved_datetime__date__lte=to_date) if to_date else user_ids
    user_ids = user_ids.values_list('user_id', flat=True)
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

        return trix_models.Tag.objects.filter(tag__in=tags)

    def get_from_date(self):
        from_date = self.request.GET.get('from')
        if from_date == '':
            from_date = None
        return from_date

    def get_to_date(self):
        to_date = self.request.GET.get('to')
        if to_date == '':
            to_date = None
        return to_date

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

    def _create_filter_object(self, howsolved_filter):
        f = Q(howsolved__howsolved=howsolved_filter)
        return f

    def _get_howsolved(self, from_date=None, to_date=None):
        queryset = trix_models.HowSolved.objects.all()
        if from_date and to_date:
            queryset = queryset.filter(solved_datetime__date__range=(from_date, to_date))
        else:
            if self.from_date is not None:
                queryset = queryset.filter(
                    solved_datetime__date__gte=self.from_date
                )
            if self.to_date is not None:
                queryset = queryset.filter(
                    solved_datetime__date__lte=self.to_date
                )

        return queryset

    def _get_usercount(self):
        assignment_id_list = self.object_list.values_list('id', flat=True)
        queryset = self._get_howsolved(self.from_date, self.to_date)
        queryset = queryset.filter(assignment_id__in=assignment_id_list).distinct('user_id')
        return queryset.values('user_id').count()

    def get_queryset(self):
        queryset = super(AssignmentStatsMixin, self).get_queryset().prefetch_related('tags')
        queryset = queryset.filter(tags__in=self.tags)

        # Filter on dates if present
        howsolved_assignment_ids = self._get_howsolved(self.from_date, self.to_date) \
            .values_list('assignment_id', flat=True)

        return queryset.filter(id__in=howsolved_assignment_ids).distinct()


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
            csvwriter = csv.writer(response, dialect='semicolons')
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
        except Exception as e:
            raise e
        return response

    def get_queryset(self):
        queryset = trix_models.Assignment.objects.all().order_by('title')
        queryset = queryset.filter(tags__in=self.tags)
        # Filter on dates if present
        from_date = self.get_from_date()
        if from_date is not None:
            queryset = queryset.filter(
                howsolved__solved_datetime__date__gte=from_date
            )
        to_date = self.get_to_date()
        if to_date is not None:
            queryset = queryset.filter(
                howsolved__solved_datetime__date__lte=to_date
            )

        queryset = queryset.distinct()
        return queryset


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
        self.from_date = self.get_from_date()
        self.to_date = self.get_to_date()
        return super(StatisticsChartView, self).get(request, *args, **kwargs)

    def _get_selectable_tags(self):
        tags = (trix_models.Tag.objects
                .filter(assignment__in=self.object_list)
                .exclude(id__in=self.tags)
                .order_by('tag')
                .distinct()
                .values_list('tag', flat=True))
        return tags

    def get_context_data(self, **kwargs):
        context = super(StatisticsChartView, self).get_context_data(**kwargs)

        context['user_count'] = self._get_usercount()
        context['selected_tags_string'] = ','.join(self.tags.values_list('tag', flat=True))
        context['selected_tags_list'] = self.tags
        context['selectable_tags_list'] = self._get_selectable_tags()
        context['course_tag'] = self.request.cradmin_role.course_tag.tag
        context['sort_list'] = ','.join(self.sort_list)
        # List of ways to sort. To add or remove ways to sort just expand or remove from this list.
        context['selectable_sort_list'] = [(_('Title'), 'title'),
                                           (_('ID'), 'id'),
                                           (_('Date created'), 'created_datetime'),
                                           (_('Last updated'), 'lastupdate_datetime')]
        context['from_date'] = self.from_date
        context['to_date'] = self.to_date
        return context

    def get_ordering(self):
        ordering = self.request.GET.get('ordering', 'id')

        if ordering is not None:
            ordering = ordering.split(',')
        return ordering


class App(crapp.App):
    appurls = [
        crapp.Url(r'^$', StatisticsChartView.as_view(), name=crapp.INDEXVIEW_NAME),
        crapp.Url(r'^ascsv$', AssignmentStatsCsv.as_view(), name='ascsv'),
    ]
