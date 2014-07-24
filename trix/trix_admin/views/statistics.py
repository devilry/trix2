from django.views.generic import ListView
from django.contrib.auth import get_user_model

from django_cradmin import crapp
from django_cradmin.viewhelpers import objecttable

from trix.trix_core import models as trix_models

# class PermalinkListView(objecttable.ObjectTableView):
#     model = trix_models.Permalink
#     columns = [
#         TitleColumn,
#         TagsColumn,
#         DescriptionIntroColumn
#     ]

#     def get_queryset_for_role(self, course):
#         return self.model.objects.filter(course=course)


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
        self.queryset = trix_models.Assignment.objects.filter(tags__id=kwargs['pk'])
        return super(StatisticsChartView, self).get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(StatisticsChartView, self).get_context_data(*args, **kwargs)
        context['user_count'] = get_user_model().objects.all().count()
        context['assignment_count'] = self.queryset.count()
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
