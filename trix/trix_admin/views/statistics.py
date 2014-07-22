from django.views.generic import TemplateView
# from django.contrib.auth import get_user_model

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


class StatisticsChartView(TemplateView):
    template_name = 'trix_admin/statistics.django.html'

    def get_context_data(self, *args, **kwargs):
        context = super(StatisticsChartView, self).get_context_data(*args, **kwargs)

        assignments = trix_models.Assignment.objects.filter(tags__id=kwargs['pk'])
        # user = get_user_model()
        # user_count = get_user_model().objects.all().count()

        total = assignments.count()
        if total > 0:
            bymyself = assignments.filter(howsolved__howsolved='bymyself').count()
            withhelp = assignments.filter(howsolved__howsolved='withhelp').count()
            notsolved = total - (bymyself + withhelp)
            context['bymyself_percent'] = int(bymyself / float(total) * 100)
            context['withhelp_percent'] = int(withhelp / float(total) * 100)
            context['notsolved_percent'] = int(notsolved / float(total) * 100)
        context['total'] = total
        context['assignment_list'] = assignments
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
